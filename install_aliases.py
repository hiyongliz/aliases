import os


def main():
    shell = os.getenv('SHELL')
    if not shell:
        raise Exception('SHELL environment variable not set')

    rc_file = None
    if shell == '/bin/bash':
        rc_filepath = os.path.expanduser('~/.bashrc')
    elif shell == '/bin/zsh':
        rc_filepath = os.path.expanduser('~/.zshrc')
    else:
        raise Exception('Unsupported shell: {}'.format(shell))

    with open(rc_filepath, 'r', encoding="utf-8") as f:
        rc_file = f.readlines()
        for line in rc_file:
            if line.strip().startswith("#"):
                continue
            if "[ -f ~/.aliases ] && source ~/.aliases" in line:
                print("Already installed")
                return

    # Move .aliases to ~/.alisase
    os.system('cp .aliases ~/.aliases')

    with open(rc_filepath, 'a', encoding="utf-8") as f:
        f.write('\n[ -f ~/.aliases ] && source ~/.aliases\n')


if __name__ == "__main__":
    main()
