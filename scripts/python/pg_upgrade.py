#!/usr/bin/env python3
"""
Minimal PostgreSQL upgrade helper for macOS + Homebrew.

Features:
1. Uses Homebrew to upgrade PostgreSQL.
2. User MUST pass old and new versions: -o OLD -n NEW
3. Uses pg_dumpall to perform backup of existing databases.
4. Stops old PostgreSQL service before upgrade.
5. Initializes new data directory if it doesn't exist or is empty.
6. Runs pg_upgrade with correct old/new bindir and datadir.
7. Logs all actions to console and log file.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from script_logger import ScriptLogger


LOG_PATH = Path.cwd() / "logs" / "pg_upgrade.log"


@dataclass(frozen=True)
class BrewPgFormulas:
    """Data class to hold PostgreSQL Homebrew formula names."""

    old: str
    new: str


@dataclass(frozen=True)
class PgPaths:
    """Data class to hold PostgreSQL paths."""

    old_bindir: Path
    old_datadir: Path
    new_bindir: Path
    new_datadir: Path


def build_pg_paths(brew_prefix: Path, brew_formulas: BrewPgFormulas) -> PgPaths:
    """Construct all relevant PostgreSQL paths from the Homebrew prefix.

    Parameters:
        brew_prefix (Path): The Homebrew installation prefix.
        brew_formulas (BrewPgFormulas): The old and new PostgreSQL formula names.

    Returns:
        PgPaths: A data class instance containing all relevant paths.
    """

    return PgPaths(
        old_bindir=brew_prefix / "opt" / brew_formulas.old / "bin",
        old_datadir=brew_prefix / "var" / brew_formulas.old,
        new_bindir=brew_prefix / "opt" / brew_formulas.new / "bin",
        new_datadir=brew_prefix / "var" / brew_formulas.new,
    )


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


def get_brew_prefix(logger: ScriptLogger) -> Path:
    """Return the Homebrew installation prefix as a Path.

    Parameters:
        logger (ScriptLogger): Logger instance for logging.

    Returns:
        Path: The Homebrew prefix path.
    """

    result = subprocess.run(
        ["brew", "--prefix"], check=True, capture_output=True, text=True
    )
    prefix = Path(result.stdout.strip())
    logger.info("Homebrew prefix: %s", prefix)
    return prefix


def run_cmd(cmd: list[str], logger: ScriptLogger) -> None:
    """Run a command and log it.

    Parameters:
        cmd (list[str]): Command and arguments to run.
        logger (ScriptLogger): Logger instance for logging.

    Returns:
        None
    """

    try:
        logger.info("Running: %s", " ".join(cmd))
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(
            "Command failed with exit code %d: %s", e.returncode, " ".join(cmd)
        )
        sys.exit(e.returncode)


def install_brew_formula(formula: str, logger: ScriptLogger) -> None:
    """Install a Homebrew formula if not already installed.

    Parameters:
        formula (str): The Homebrew formula name to check and install.
        logger (ScriptLogger): Logger instance for logging.

    Returns:
        None
    """

    logger.info("Ensuring %s is installed via Homebrew...", formula)
    result = subprocess.run(
        ["brew", "list", "--versions", formula],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        logger.info("%s not installed. Installing with Homebrew...", formula)
        run_cmd(["brew", "install", formula], logger)
    else:
        logger.info("%s already installed.", formula)


def backup_pg_databases(pg_dumpall: Path, backup_file: Path, logger: ScriptLogger) -> None:
    """Back up all databases using pg_dumpall.

    Parameters:
        pg_dumpall (Path): Path to the pg_dumpall binary.
        backup_file (Path): Destination file for the SQL dump.
        logger (ScriptLogger): Logger instance for logging.

    Returns:
        None
    """

    logger.info("Creating backup with %s", pg_dumpall)
    logger.info("Backup file: %s", backup_file)

    try:
        with backup_file.open("w", encoding="utf-8") as file_obj:
            subprocess.run([str(pg_dumpall)], check=True, stdout=file_obj)
    except subprocess.CalledProcessError as e:
        logger.error("Backup failed. Removing partial file: %s", backup_file)
        backup_file.unlink(missing_ok=True)
        sys.exit(e.returncode)

    logger.info("Backup complete.")


def init_new_datadir(initdb: Path, datadir: Path, logger: ScriptLogger) -> None:
    """Initialize new PostgreSQL data directory if it doesn't exist or is empty.

    Parameters:
        initdb (Path): Path to the initdb binary.
        datadir (Path): Path to the new data directory.
        logger (ScriptLogger): Logger instance for logging.

    Returns:
        None
    """

    logger.info("Initializing new data directory (if empty): %s", datadir)

    if not datadir.exists() or not any(datadir.iterdir()):
        run_cmd([str(initdb), "-D", str(datadir)], logger)
    else:
        logger.info("Data directory exists; skipping initdb.")


def main() -> int:
    """Entry point. Orchestrates the update process.

    Parameters:
        None

    Returns:
        int: Exit code (0 for success).
    """

    # 1.0 CLI arguments
    args = parse_args()
    old_ver = args.old_version
    new_ver = args.new_version

    # 2.0 Logger setup
    logger = ScriptLogger.log_to_console_and_file(
        "pg_upgrade", log_file=LOG_PATH, colorize=True
    )
    logger.info("Logging to %s", LOG_PATH)

    # 3.0 Start upgrade process
    logger.info("Starting PostgreSQL upgrade: %s -> %s", old_ver, new_ver)

    # 4.0 Get Homebrew prefix
    brew_prefix = get_brew_prefix(logger)

    # 5.0 Build relevant paths
    brew_pg_formulas = BrewPgFormulas(
        old=f"postgresql@{old_ver}", new=f"postgresql@{new_ver}"
    )
    pg_paths = build_pg_paths(brew_prefix, brew_pg_formulas)

    logger.info("Old bindir: %s", pg_paths.old_bindir)
    logger.info("New bindir: %s", pg_paths.new_bindir)
    logger.info("Old datadir: %s", pg_paths.old_datadir)
    logger.info("New datadir: %s", pg_paths.new_datadir)

    # 6.0 Install new version of postgreSQL if not already installed
    install_brew_formula(brew_pg_formulas.new, logger)

    # 7.0 Ensure old PostgreSQL service is running for backup
    logger.info(
        "Ensure old PostgreSQL service is running for backup operation: %s",
        brew_pg_formulas.old,
    )

    # If it's already running, this is a no-op; if not, it starts it.
    run_cmd(["brew", "services", "start", brew_pg_formulas.old], logger)

    # 8.0 Backup existing data with pg_dumpall
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = Path.home() / f"pg_dumpall_{old_ver}_to_{new_ver}_{timestamp}.sql"
    backup_pg_databases(pg_paths.old_bindir / "pg_dumpall", backup_file, logger)

    # 9.0 Stop PostgreSQL service
    run_cmd(["brew", "services", "stop", brew_pg_formulas.old], logger)

    # 10. Initialize new data directory if it doesn't exist or is empty
    init_new_datadir(pg_paths.new_bindir / "initdb", pg_paths.new_datadir, logger)

    # 11. Run pg_upgrade
    logger.info("Running pg_upgrade...")
    run_cmd(
        [
            str(pg_paths.new_bindir / "pg_upgrade"),
            f"--old-bindir={pg_paths.old_bindir}",
            f"--new-bindir={pg_paths.new_bindir}",
            f"--old-datadir={pg_paths.old_datadir}",
            f"--new-datadir={pg_paths.new_datadir}",
        ],
        logger,
    )

    # 12. Start new PostgreSQL service
    run_cmd(["brew", "services", "start", brew_pg_formulas.new], logger)

    logger.info("Upgrade complete: %s -> %s", old_ver, new_ver)
    logger.info("Backup stored at: %s", backup_file)

    logger.warning(
        "Update zsh/env.zsh PATH variable to new postgresql@%s/bin.", new_ver
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
