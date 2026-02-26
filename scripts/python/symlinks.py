#!/usr/bin/env python3
import pathlib
import shutil

from script_logger import ScriptLogger

HOME: pathlib.Path = pathlib.Path("/Users/arwhyte")
BASE_PATH: pathlib.Path = HOME / "Development/github/arwhyte/dotfiles-m1"
LINKS: tuple[tuple[pathlib.Path, pathlib.Path], ...] = (
    # (HOME / "brew.sh", BASE_PATH / "scripts/shell/brew.sh"),
    (HOME / ".gitconfig", BASE_PATH / "git/.gitconfig"),
    # (HOME / ".gitconfig.local", BASE_PATH / "git/.gitconfig.local"),
    # (HOME / ".gitignore.global", BASE_PATH / "git/.gitignore.global"),
    (HOME / ".psqlrc", BASE_PATH / "psql/.psqlrc"),
    # (HOME / "update.sh", BASE_PATH / "scripts/shell/update.sh"),
    (HOME / "pg_upgrade.py", BASE_PATH / "scripts/python/pg_upgrade.py"),
    (HOME / "update.py", BASE_PATH / "scripts/python/update.py"),
    (HOME / ".zprofile", BASE_PATH / "zsh/.zprofile"),
    (HOME / ".zshenv", BASE_PATH / "zsh/.zshenv"),
    (HOME / ".zshrc", BASE_PATH / "zsh/.zshrc"),
)


def create_symlink(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Remove destination (dst) if it exists, then create a symlink at dst → src.
    Equivalent to: rm -rf dst; ln -nfs src dst

    Parameters
        src : pathlib.Path
        dst : pathlib.Path

    Returns
        None
    """

    if dst.exists() or dst.is_symlink():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    dst.symlink_to(src)


def main() -> None:
    """Entry point for the script. Creates symlinks for all paths in LINKS.

    Parameters
        None

    Returns
        None
    """

    log = ScriptLogger("symlinks", log_to_console=True)

    for dst, src in LINKS:
        log.info(f"Linking {dst} → {src}")
        create_symlink(src, dst)


if __name__ == "__main__":
    main()
