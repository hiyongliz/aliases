import logging
import os
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def copy_alias_file() -> None:
    # Copy the .aliases file to the home directory
    home_dir: Path = Path.home()
    aliases_path: Path = home_dir / ".aliases"

    aliases_file = []
    for file in Path(".").iterdir():
        if file.name.startswith(".") and file.name.endswith("aliases"):
            aliases_file.append(file)
    if not aliases_file:
        raise Exception("No alias file found in the current directory.")

    aliases_content = ""
    for file in aliases_file:
        with open(file, "r", encoding="utf-8") as f:
            aliases_content += f"# {file}\n"
            aliases_content += f.read()
            aliases_content += "\n"

    with open(aliases_path, "w", encoding="utf-8") as f:
        f.write(aliases_content)


def main() -> None:
    # Backup existing .aliases file
    home_dir: Path = Path.home()
    aliases_path: Path = home_dir / ".aliases"
    if aliases_path.exists():
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path: Path = home_dir / f".aliases.bak.{timestamp}"
        aliases_path.rename(backup_path)
        logging.info(f"Backup of existing .aliases created at {backup_path}")
    else:
        logging.info("No existing .aliases file found.")

    # Copy new .aliases file
    copy_alias_file()

    shell: str | None = os.getenv("SHELL")
    if not shell:
        raise Exception("SHELL environment variable not set.")

    rc_filepath: Path = home_dir / f".{shell.split('/')[-1]}rc"

    with open(rc_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("#"):
            continue
        if "[ -f ~/.aliases ] && source ~/.aliases" in line:
            logging.info("Done!")
            return

    logging.info("Adding source command to shell configuration file...")
    with open(rc_filepath, "a", encoding="utf-8") as f:
        f.write("\n[ -f ~/.aliases ] && source ~/.aliases\n")

    logging.info("Done!")


if __name__ == "__main__":
    main()
