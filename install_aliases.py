import os
from datetime import datetime


def copy_alias_file():
    # Copy the .aliases file to the home directory
    home_dir = os.path.expanduser("~")
    aliases_path = os.path.join(home_dir, ".aliases")

    aliases_file = []
    for file in os.listdir(os.getcwd()):
        if file.startswith(".") and file.endswith("aliases"):
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


def main():
    # Backup existing .aliases file
    home_dir = os.path.expanduser("~")
    aliases_path = os.path.join(home_dir, ".aliases")
    if os.path.exists(aliases_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join(home_dir, f".aliases.bak.{timestamp}")
        os.rename(aliases_path, backup_path)
        print(f"Backup of existing .aliases created at {backup_path}")
    else:
        print("No existing .aliases file found.")

    # Copy new .aliases file
    copy_alias_file()

    shell = os.getenv("SHELL")
    if not shell:
        raise Exception("SHELL environment variable not set.")

    if shell.endswith("/bash"):
        rc_filepath = os.path.expanduser("~/.bashrc")
    elif shell.endswith("/zsh"):
        rc_filepath = os.path.expanduser("~/.zshrc")
    else:
        raise Exception("Unsupported shell: {}.".format(shell))

    with open(rc_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("#"):
            continue
        if "[ -f ~/.aliases ] && source ~/.aliases" in line:
            print("Done!")
            return

    print("Adding source command to shell configuration file...")
    with open(rc_filepath, "a", encoding="utf-8") as f:
        f.write("\n[ -f ~/.aliases ] && source ~/.aliases\n")

    print("Done!")


if __name__ == "__main__":
    main()
