#!/usr/bin/env python3
"""
Update Astral uv, uv tools, and Homebrew installs.

This script is the Python equivalent of:

1. scripts/uv.sh
2. scripts/brew.sh
3. the wrapper script that calls both
"""

import subprocess
import sys

from pathlib import Path
from script_logger import ScriptLogger


HOME = Path.home()
BREWFILE_PATH = HOME / "Development/github/arwhyte/dotfiles-m1/brew/Brewfile"


def run_cmd(cmd: list[str], logger: ScriptLogger, ignore_errors: bool = False) -> None:
    """Run a command, streaming output directly.
    Exit immediately if the command fails (set -e behavior), unless ignore_errors is True.

    Parameters:
        cmd (list[str]): Command and arguments to run.
        logger: The logger instance to use for logging messages.
        ignore_errors (bool): If True, log errors but do not exit on failure.

    Returns:
        None
    """

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            logger.warning("Command exited with %s: %s", e.returncode, " ".join(cmd))
        else:
            logger.error(
                "Command failed with exit code %d: %s", e.returncode, " ".join(cmd)
            )
            sys.exit(e.returncode)


def update_brew(logger: ScriptLogger) -> None:
    """Replicates brew.sh behavior.

    Parameters:
        logger: The logger instance to use for logging messages.

    Returns:
        None
    """

    logger.info("HOMEBREW INSTALLED PACKAGES/CASKS (brew list)")
    run_cmd(["brew", "list"], logger)

    logger.info("HOMEBREW OUTDATED PACKAGES/CASKS (brew outdated)")
    run_cmd(["brew", "outdated"], logger)

    logger.info("AUTOREMOVE UNUSED PACKAGE DEPENDENCIES (brew autoremove)")
    run_cmd(["brew", "autoremove"], logger)

    logger.info("UPDATE HOMEBREW PACKAGES/CASKS (brew update)")
    run_cmd(["brew", "update"], logger)

    logger.info("UPGRADE HOMEBREW PACKAGES/CASKS (brew upgrade --greedy)")
    run_cmd(["brew", "upgrade", "--greedy"], logger)

    logger.info("CHECK HOMEBREW INSTALLS (brew doctor)")
    run_cmd(["brew", "doctor"], logger, ignore_errors=True)

    logger.info("CLEANUP HOMEBREW (brew cleanup)")
    run_cmd(["brew", "cleanup"], logger)

    logger.info("DUMP HOMEBREW INSTALLS TO %s (brew bundle dump)", BREWFILE_PATH)
    run_cmd(["brew", "bundle", "dump", "--force", f"--file={BREWFILE_PATH}"], logger)

    logger.info("HOMEBREW MANAGED SERVICES (brew services list)")
    run_cmd(["brew", "services", "list"], logger)


def update_uv(logger: ScriptLogger) -> None:
    """Replicates uv.sh behavior.

    Parameters:
        logger: The logger instance to use for logging messages.

    Returns:
        None
    """

    logger.info("UPDATE UV")
    run_cmd(["uv", "self", "update"], logger)

    logger.info("UPDATE UV TOOLS")
    run_cmd(["uv", "tool", "update", "--all"], logger)


def main() -> None:
    """Entry point. Orchestrates the update process.

    Parameters:
        None

    Returns:
        None
    """

    logger = ScriptLogger.log_to_console("update", colorize=True)

    logger.info("STARTING UV AND BREW UPDATE/UPGRADE.")

    logger.info("UPDATE ASTRAL UV AND UV TOOL (ALL)")
    update_uv(logger)

    logger.info("UPDATE/UPGRADE HOMEBREW PACKAGES/CASKS")
    update_brew(logger)


if __name__ == "__main__":
    main()
