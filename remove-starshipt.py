#!/bin/env python3
import os
import sys
import shlex

RED = "\033[31m"
RESET = "\033[0m"


def get_target_home() -> str:
    sudo_user = os.environ.get("SUDO_USER")
    if not sudo_user:
        print(f"\n{RED}SUDO_USER not set. Run with sudo, e.g. 'sudo python3 remove-starship.py'.{RESET}\n")
        sys.exit(1)
    return f"/home/{sudo_user}"


def run(cmd: str) -> bool:
    """Run a shell command and return True if it succeeded."""
    result = os.system(cmd)
    return result == 0


def remove_files(home: str) -> None:
    safe_home = shlex.quote(home)

    targets = [
        f"rm -rf {safe_home}/.config/starship.toml",
        f"rm -rf {safe_home}/.cache/starship",
        "rm -rf /usr/local/bin/starship",
    ]

    starship_config = os.environ.get("STARSHIP_CONFIG")
    if starship_config:
        targets.append(f"rm -rf {shlex.quote(starship_config)}")

    starship_cache = os.environ.get("STARSHIP_CACHE")
    if starship_cache:
        targets.append(f"rm -rf {shlex.quote(starship_cache)}")

    for cmd in targets:
        if not run(cmd):
            print(f"\n{RED}Failed to run: {cmd}{RESET}\n")


def remove_line_from_file(filepath: str, pattern: str) -> None:
    """Remove a matching line from a file only if the file exists."""
    if not os.path.exists(filepath):
        return
    safe_path = shlex.quote(filepath)
    safe_pattern = pattern.replace("/", "\\/")
    cmd = f"sed -i -e '/{safe_pattern}/d' {safe_path}"
    if not run(cmd):
        print(f"\n{RED}Failed to update: {filepath}{RESET}\n")


def update_files(home: str) -> None:
    shell_configs = [
        (f"{home}/.bashrc",                   'eval "$(starship init bash)"'),
        (f"{home}/.elvish/rc.elv",            'eval (starship init elvish)'),
        (f"{home}/.config/fish/config.fish",  'starship init fish | source'),
        (f"{home}/.config/ion/initrc",        'eval $(starship init ion)'),
        (f"{home}/.tcshrc",                   'eval `starship init tcsh`'),
        (f"{home}/.xonshrc",                  'execx($(starship init xonsh))'),
        (f"{home}/.zshrc",                    'eval "$(starship init zsh)"'),
    ]

    for filepath, pattern in shell_configs:
        remove_line_from_file(filepath, pattern)


def main() -> None:
    home = get_target_home()
    remove_files(home)
    update_files(home)
    print("\nStarship removal complete.\n")


if __name__ == "__main__":
    if os.getuid() != 0:
        print(f"\n{RED}Please run as root (use sudo).{RESET}\n")
        sys.exit(1)
    main()
