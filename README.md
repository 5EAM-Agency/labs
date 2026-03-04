# starship-uninstall

A lightweight Python utility to fully remove [Starship](https://starship.rs) from a Linux system — including its binary, config files, cache, and shell init hooks.

---

## What It Does

Running this script will:

- Remove the Starship binary from `/usr/local/bin/starship`
- Delete Starship's config file (`~/.config/starship.toml`) and cache (`~/.cache/starship`)
- Strip the Starship init hook from the following shell config files, if present:

  | Shell   | Config File                        |
  |---------|------------------------------------|
  | Bash    | `~/.bashrc`                        |
  | Zsh     | `~/.zshrc`                         |
  | Fish    | `~/.config/fish/config.fish`       |
  | Elvish  | `~/.elvish/rc.elv`                 |
  | Ion     | `~/.config/ion/initrc`             |
  | Tcsh    | `~/.tcshrc`                        |
  | Xonsh   | `~/.xonshrc`                       |

---

## Requirements

- Python 3
- Linux (tested on Ubuntu)
- Must be run as **root** (via `sudo`)

---

## Usage

```bash
sudo python3 starship_uninstall.py
```

> The script uses `SUDO_USER` to correctly resolve the home directory of the invoking user, so running with `sudo` is required — not optional.

---

## Notes

- This script modifies shell config files in-place using `sed`. It targets only the specific Starship init lines and leaves the rest of each file untouched.
- Environment variables `$STARSHIP_CONFIG` and `$STARSHIP_CACHE` are also cleared if set to non-default paths.
- If any step fails, the script will print an error message in red and continue — it will not abort the entire run.

---

## Disclaimer

This is an experimental fork, not the official Starship uninstaller. Always review scripts before running them as root. Back up your shell config files if you're unsure.

---

## License

MIT
