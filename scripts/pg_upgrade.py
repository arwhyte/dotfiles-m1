#!/usr/bin/env python3
"""
Minimal PostgreSQL upgrade helper for macOS + Homebrew.

Requirements:
1. Use Homebrew to upgrade PostgreSQL.
2. User MUST pass old and new versions: -o OLD -n NEW
3. Use pg_dumpall to perform backup of existing databases.
4. Stop old PostgreSQL service before upgrade.
5. Initialize new data directory if it doesn't exist or is empty.
6. Run pg_upgrade with correct old/new bindir and datadir.
7. Log all actions to terminal + log file.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters:
        None

    Returns:
        argparse.Namespace: Parsed arguments with 'old_version' and 'new_version' attributes.
    """

    parser = argparse.ArgumentParser(description="Simple PostgreSQL upgrader.")
    parser.add_argument(
        "-o",
        "--old-version",
        required=True,
        help="Old PostgreSQL major version (e.g., 17)",
    )
    parser.add_argument(
        "-n",
        "--new-version",
        required=True,
        help="New PostgreSQL major version (e.g., 18)",
    )
    return parser.parse_args()


def setup_logger(old_ver: str, new_ver: str) -> logging.Logger:
    """Set up logging to console and file.

    Parameters:
        old_ver (str): Old PostgreSQL version.
        new_ver (str): New PostgreSQL version.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger("pg_upgrade")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_file = Path.cwd() / f"pg_upgrade_{old_ver}_to_{new_ver}.log"

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # file
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Logging to %s", log_file)
    return logger


def run(cmd: list[str], logger: logging.Logger) -> None:
    """Run a command and log it.

    Parameters:
        cmd (list[str]): Command and arguments to run.
        logger (logging.Logger): Logger instance for logging.

    Returns:
        None
    """
    logger.info("Running: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    """Main function to perform PostgreSQL upgrade.

    Parameters:
        None

    Returns:
        int: Exit code (0 for success).
    """

    args = parse_args()
    old_ver = args.old_version
    new_ver = args.new_version

    logger = setup_logger(old_ver, new_ver)
    logger.info("Starting PostgreSQL upgrade: %s -> %s", old_ver, new_ver)

    # Homebrew prefix
    brew_prefix = subprocess.run(
        ["brew", "--prefix"], check=True, stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    logger.info("Homebrew prefix: %s", brew_prefix)

    old_formula = f"postgresql@{old_ver}"
    new_formula = f"postgresql@{new_ver}"

    # old_bindir = Path(brew_prefix) / f"opt/{old_formula}/bin"
    old_bindir = Path(brew_prefix).joinpath("opt", old_formula, "bin")

    # new_bindir = Path(brew_prefix) / f"opt/{new_formula}/bin"
    new_bindir = Path(brew_prefix).joinpath("opt", new_formula, "bin")

    # old_datadir = Path(brew_prefix) / f"var/postgresql@{old_ver}"
    old_datadir = Path(brew_prefix).joinpath("var", f"postgresql@{old_ver}")

    # new_datadir = Path(brew_prefix) / f"var/postgresql@{new_ver}"
    new_datadir = Path(brew_prefix).joinpath("var", f"postgresql@{new_ver}")

    logger.info("Old bindir: %s", old_bindir)
    logger.info("New bindir: %s", new_bindir)
    logger.info("Old datadir: %s", old_datadir)
    logger.info("New datadir: %s", new_datadir)

    # Install new version of postgreSQL if not already installed
    logger.info("Ensuring %s is installed via Homebrew...", new_formula)
    result_new = subprocess.run(
        ["brew", "list", "--versions", new_formula],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result_new.returncode != 0:
        logger.info("%s not installed. Installing with Homebrew...", new_formula)
        run(["brew", "install", new_formula], logger)
    else:
        logger.info("%s already installed.", new_formula)

    # Refresh new_bindir now that we’re sure it’s installed
    new_bindir = Path(brew_prefix).joinpath("opt", new_formula, "bin")

    # Ensure old PostgreSQL service is running for backup
    logger.info(
        "Ensuring old PostgreSQL service is running for backup: %s", old_formula
    )
    # If it's already running, this is a no-op; if not, it starts it.
    run(["brew", "services", "start", old_formula], logger)

    # Backup existing data with pg_dumpall
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # backup_file = Path.home() / f"pg_dumpall_{old_ver}_to_{new_ver}_{timestamp}.sql"
    backup_file = Path.home().joinpath(
        f"pg_dumpall_{old_ver}_to_{new_ver}_{timestamp}.sql"
    )

    # pg_dumpall = old_bindir / "pg_dumpall"
    pg_dumpall = old_bindir.joinpath("pg_dumpall")

    logger.info("Creating backup with %s", pg_dumpall)
    logger.info("Backup file: %s", backup_file)

    with backup_file.open("w", encoding="utf-8") as f:
        subprocess.run([str(pg_dumpall)], check=True, stdout=f)

    logger.info("Backup complete.")

    # Stop PostgreSQL service
    run(["brew", "services", "stop", old_formula], logger)

    # Initialize new data directory if it doesn't exist or is empty
    initdb = new_bindir / "initdb"
    logger.info("Initializing new data directory (if empty): %s", new_datadir)

    if not new_datadir.exists() or not any(new_datadir.iterdir()):
        run([str(initdb), "-D", str(new_datadir)], logger)
    else:
        logger.info("Data directory exists; skipping initdb.")

    # Run pg_upgrade
    pg_upgrade = new_bindir / "pg_upgrade"
    logger.info("Running pg_upgrade...")
    run(
        [
            str(pg_upgrade),
            f"--old-bindir={old_bindir}",
            f"--new-bindir={new_bindir}",
            f"--old-datadir={old_datadir}",
            f"--new-datadir={new_datadir}",
        ],
        logger,
    )

    # Start new PostgreSQL service
    run(["brew", "services", "start", new_formula], logger)

    logger.info("Upgrade complete: %s -> %s", old_ver, new_ver)
    logger.info("Backup stored at: %s", backup_file)

    logger.info(
        f"WARN: Update zsh/env.zsh PATH variable to new postgresql@{new_ver}/bin."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
