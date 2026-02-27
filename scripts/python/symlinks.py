#!/usr/bin/env python3
import pathlib
import shutil

from dataclasses import dataclass
from script_logger import ScriptLogger


HOME: pathlib.Path = pathlib.Path.home()
BASE_PATH: pathlib.Path = HOME / "Development/github/arwhyte/dotfiles-m1"
GIT_PATH: pathlib.Path = BASE_PATH / "git"
PSQL_PATH: pathlib.Path = BASE_PATH / "psql"
PY_SCRIPTS_PATH: pathlib.Path = BASE_PATH / "scripts/python"
ZSH_PATH: pathlib.Path = BASE_PATH / "zsh"


@dataclass(frozen=True)
class SymlinkPair:
    src: pathlib.Path
    dst: pathlib.Path

    def __post_init__(self) -> None:
        """Validate that src and dst are pathlib.Path instances and that src exists.

        Parameters:
            None

        Returns:
            None

        Raises:
            TypeError: If src or dst are not pathlib.Path instances.
            FileNotFoundError: If src does not exist.
        """

        if not isinstance(self.src, pathlib.Path):
            raise TypeError(f"src must be a pathlib.Path, got {type(self.src)}")
        if not isinstance(self.dst, pathlib.Path):
            raise TypeError(f"dst must be a pathlib.Path, got {type(self.dst)}")
        if not self.src.exists():
            raise FileNotFoundError(f"Source path does not exist: {self.src}")


def create_symlink(pair: SymlinkPair) -> None:
    """Remove destination (dst) if it exists, then create a symlink at dst.
    Equivalent to: rm -rf dst; ln -nfs src dst

    Parameters:
        pair (SymlinkPair): The source and destination paths to link.

    Returns:
        None
    """

    if pair.dst.exists() or pair.dst.is_symlink():
        if pair.dst.is_dir() and not pair.dst.is_symlink():
            shutil.rmtree(pair.dst)
        else:
            pair.dst.unlink()
    pair.dst.symlink_to(pair.src)


def main() -> None:
    """Entry point for the script. Creates symlinks for all paths in path_pairs.

    Parameters:
        None

    Returns:
        None
    """

    log = ScriptLogger("symlinks", log_to_console=True, colorize=True)

    path_pairs: tuple[SymlinkPair, ...] = (
        SymlinkPair(src=GIT_PATH / ".gitconfig", dst=HOME / ".gitconfig"),
        SymlinkPair(src=PSQL_PATH / ".psqlrc", dst=HOME / ".psqlrc"),
        SymlinkPair(src=ZSH_PATH / ".zprofile", dst=HOME / ".zprofile"),
        SymlinkPair(src=ZSH_PATH / ".zshenv", dst=HOME / ".zshenv"),
        SymlinkPair(src=ZSH_PATH / ".zshrc", dst=HOME / ".zshrc"),
        SymlinkPair(src=PY_SCRIPTS_PATH / "pg_upgrade.py", dst=HOME / "pg_upgrade.py"),
        SymlinkPair(src=PY_SCRIPTS_PATH / "update.py", dst=HOME / "update.py"),
    )

    for pair in path_pairs:
        try:
            log.info(f"Linking {pair.dst} → {pair.src}")
            create_symlink(pair)
        except (FileNotFoundError, PermissionError) as e:
            log.error(f"Failed: {e}")


if __name__ == "__main__":
    main()
