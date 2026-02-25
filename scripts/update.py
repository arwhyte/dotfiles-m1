#!/usr/bin/env python3
"""
Update Astral uv, uv tools, and Homebrew installs.

This script is the Python equivalent of:

- scripts/uv.sh
- scripts/brew.sh
- the wrapper script that calls both
"""

import logging
import subprocess
import sys

from pathlib import Path


HOME = Path.home()
BREWFILE_PATH = HOME.joinpath("Development/github/arwhyte/dotfiles-m1/brew/Brewfile")
LOGGER = logging.getLogger("update")


def run_cmd(cmd: list[str], ignore_errors: bool = False) -> None:
    """Run a command, streaming output directly.
    Exit immediately if the command fails (set -e behavior), unless ignore_errors is True.

    Parameters:
        cmd (list[str]): Command and arguments to run.
        ignore_errors (bool): If True, log errors but do not exit on failure.

    Returns:
        None
    """

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            LOGGER.warning("Command exited with %s: %s", e.returncode, " ".join(cmd))
        else:
            LOGGER.error(
                "Command failed with exit code %d: %s", e.returncode, " ".join(cmd)
            )
            sys.exit(e.returncode)


def update_brew() -> None:
    """Replicates brew.sh behavior.

    Parameters:
        None

    Returns:
        None
    """

    LOGGER.info("HOMEBREW INSTALLED PACKAGES/CASKS (brew list)")
    run_cmd(["brew", "list"])

    LOGGER.info("HOMEBREW OUTDATED PACKAGES/CASKS (brew outdated)")
    run_cmd(["brew", "outdated"])

    LOGGER.info("AUTOREMOVE UNUSED PACKAGE DEPENDENCIES (brew autoremove)")
    run_cmd(["brew", "autoremove"])

    LOGGER.info("UPDATE HOMEBREW PACKAGES/CASKS (brew update)")
    run_cmd(["brew", "update"])

    LOGGER.info("UPGRADE HOMEBREW PACKAGES/CASKS (brew upgrade --greedy)")
    run_cmd(["brew", "upgrade", "--greedy"])

    LOGGER.info("CHECK HOMEBREW INSTALLS (brew doctor)")
    run_cmd(["brew", "doctor"], ignore_errors=True)

    LOGGER.info("CLEANUP HOMEBREW (brew cleanup)")
    run_cmd(["brew", "cleanup"])

    LOGGER.info(f"DUMP HOMEBREW INSTALLS TO {BREWFILE_PATH} (brew bundle dump)")
    run_cmd(
        [
            "brew",
            "bundle",
            "dump",
            "--force",
            f"--file={BREWFILE_PATH}",
        ]
    )

    LOGGER.info("HOMEBREW MANAGED SERVICES (brew services list)")
    run_cmd(["brew", "services", "list"])


def update_uv() -> None:
    """Replicates uv.sh behavior.

    Parameters:
        None

    Returns:
        None
    """

    LOGGER.info("UPDATE UV")
    run_cmd(["uv", "self", "update"])

    LOGGER.info("UPDATE UV TOOLS")
    run_cmd(["uv", "tool", "update", "--all"])


def main() -> None:
    """Entry point. Orchestrates the update process.

    Parameters:
        None

    Returns:
        None
    """

    if not LOGGER.handlers:  # already configured
        LOGGER.setLevel(logging.INFO)
        LOGGER.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        # Console
        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)

    LOGGER.info("Starting uv and brew update.")

    LOGGER.info("UPDATE ASTRAL UV AND UV TOOL (ALL)")
    update_uv()

    LOGGER.info("UPDATE/UPGRADE HOMEBREW PACKAGES/CASKS")
    update_brew()


if __name__ == "__main__":
    main()
