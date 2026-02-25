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

LOGGER = logging.getLogger("pg_upgrade")


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


def run_cmd(cmd: list[str], logger: logging.Logger) -> None:
    """Run a command and log it.

    Parameters:
        cmd (list[str]): Command and arguments to run.
        logger (logging.Logger): Logger instance for logging.

    Returns:
        None
    """

    try:
        logger.info("Running: %s", " ".join(cmd))
        subprocess.run_cmd(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(
            "Command failed with exit code %d: %s", e.returncode, " ".join(cmd)
        )
        sys.exit(e.returncode)


def main() -> int:
    """Entry point. Orchestrates the update process.

    Parameters:
        None

    Returns:
        int: Exit code (0 for success).
    """

    args = parse_args()
    old_ver = args.old_version
    new_ver = args.new_version

    if not LOGGER.handlers:  # check if already configured
        LOGGER.setLevel(logging.INFO)
        LOGGER.propagate = False

        log_file = Path.cwd().joinpath(f"pg_upgrade_{old_ver}_to_{new_ver}.log")

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        # console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        LOGGER.addHandler(stream_handler)

        # file
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        LOGGER.addHandler(file_handler)

    LOGGER.info("Logging to %s", log_file)

    LOGGER.info("Starting PostgreSQL upgrade: %s -> %s", old_ver, new_ver)

    # Homebrew prefix
    brew_prefix = subprocess.run_cmd(
        ["brew", "--prefix"], check=True, stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    LOGGER.info("Homebrew prefix: %s", brew_prefix)

    old_formula = f"postgresql@{old_ver}"
    new_formula = f"postgresql@{new_ver}"

    old_bindir = Path(brew_prefix).joinpath("opt", old_formula, "bin")
    new_bindir = Path(brew_prefix).joinpath("opt", new_formula, "bin")

    LOGGER.info("Old bindir: %s", old_bindir)
    LOGGER.info("New bindir: %s", new_bindir)

    old_datadir = Path(brew_prefix).joinpath("var", f"postgresql@{old_ver}")
    new_datadir = Path(brew_prefix).joinpath("var", f"postgresql@{new_ver}")

    LOGGER.info("Old datadir: %s", old_datadir)
    LOGGER.info("New datadir: %s", new_datadir)

    # Install new version of postgreSQL if not already installed
    LOGGER.info("Ensuring %s is installed via Homebrew...", new_formula)

    result_new = subprocess.run_cmd(
        ["brew", "list", "--versions", new_formula],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    if result_new.returncode != 0:
        LOGGER.info("%s not installed. Installing with Homebrew...", new_formula)
        run_cmd(["brew", "install", new_formula], LOGGER)
    else:
        LOGGER.info("%s already installed.", new_formula)

    # Refresh new_bindir now that we’re sure it’s installed
    new_bindir = Path(brew_prefix).joinpath("opt", new_formula, "bin")

    # Ensure old PostgreSQL service is running for backup
    LOGGER.info(
        "Ensuring old PostgreSQL service is running for backup: %s", old_formula
    )

    # If it's already running, this is a no-op; if not, it starts it.
    run_cmd(["brew", "services", "start", old_formula], LOGGER)

    # Backup existing data with pg_dumpall
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = Path.home().joinpath(
        f"pg_dumpall_{old_ver}_to_{new_ver}_{timestamp}.sql"
    )

    # pg_dumpall = old_bindir / "pg_dumpall"
    pg_dumpall = old_bindir.joinpath("pg_dumpall")

    LOGGER.info("Creating backup with %s", pg_dumpall)
    LOGGER.info("Backup file: %s", backup_file)

    with backup_file.open("w", encoding="utf-8") as f:
        subprocess.run_cmd([str(pg_dumpall)], check=True, stdout=f)

    LOGGER.info("Backup complete.")

    # Stop PostgreSQL service
    run_cmd(["brew", "services", "stop", old_formula], LOGGER)

    # Initialize new data directory if it doesn't exist or is empty
    initdb = new_bindir / "initdb"
    LOGGER.info("Initializing new data directory (if empty): %s", new_datadir)

    if not new_datadir.exists() or not any(new_datadir.iterdir()):
        run_cmd([str(initdb), "-D", str(new_datadir)], LOGGER)
    else:
        LOGGER.info("Data directory exists; skipping initdb.")

    # Run pg_upgrade
    pg_upgrade = new_bindir / "pg_upgrade"
    LOGGER.info("Running pg_upgrade...")
    run_cmd(
        [
            str(pg_upgrade),
            f"--old-bindir={old_bindir}",
            f"--new-bindir={new_bindir}",
            f"--old-datadir={old_datadir}",
            f"--new-datadir={new_datadir}",
        ],
        LOGGER,
    )

    # Start new PostgreSQL service
    run_cmd(["brew", "services", "start", new_formula], LOGGER)

    LOGGER.info("Upgrade complete: %s -> %s", old_ver, new_ver)
    LOGGER.info("Backup stored at: %s", backup_file)

    LOGGER.info(
        f"WARN: Update zsh/env.zsh PATH variable to new postgresql@{new_ver}/bin."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
