import logging
import os
from datetime import datetime
from itertools import chain
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def copy_alias_file() -> None:
    # Copy the .aliases file to the home directory
    home_dir: Path = Path.home()
    aliases_path: Path = home_dir / ".aliases"

    p = Path()
    aliases_file = chain(p.glob("*aliases.sh"), p.glob("*aliases"))
    aliases_content: list[str] = []
    for file in list(aliases_file):
        with file.open(encoding="utf-8") as f:
            aliases_content.append(f"# {file}")
            aliases_content.append(f.read())

    with aliases_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(aliases_content))


def backup_existing_aliases() -> None:
    home_dir: Path = Path.home()
    aliases_path: Path = home_dir / ".aliases"
    if aliases_path.exists():
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path: Path = home_dir / f".aliases.bak.{timestamp}"
        aliases_path.rename(backup_path)
        logging.info(f"Backup of existing .aliases created at {backup_path}")
    else:
        logging.info("No existing .aliases file found.")


def add_source_command() -> None:
    shell: str | None = os.getenv("SHELL")
    if not shell:
        raise Exception("SHELL environment variable not set.")

    rc_filepath: Path = Path.home() / f".{shell.split('/')[-1]}rc"
    with rc_filepath.open("r", encoding="utf-8") as f:
        lines: list[str] = f.readlines()

    for line in lines:
        if line.strip().startswith("#"):
            continue
        if "[ -f ~/.aliases ] && source ~/.aliases" in line:
            return

    logging.info("Adding source command to shell configuration file...")
    with rc_filepath.open("a", encoding="utf-8") as f:
        f.write("\n[ -f ~/.aliases ] && source ~/.aliases\n")


def main() -> None:
    # Backup existing .aliases file
    backup_existing_aliases()

    # Copy new .aliases file
    copy_alias_file()

    # Add source command to shell configuration file
    add_source_command()

    logging.info("Done!")


if __name__ == "__main__":
    main()
