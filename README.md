# Jumpboot

A CLI tool that opens all your apps and links with one command, so you can start a study or work session without getting distracted first.

```
jmp tryhackme
```

One command, and your course video, notes, and tools all open together.

## Why

Every time I sat down to study, I'd lose ten minutes opening the wrong tab, getting sidetracked, and deciding what to open first. Jumpboot lets you decide that once, save it as a **workflow**, and launch the whole setup whenever you need it.

## Install

### Windows (winget)

```
winget install KushChandak.Jumpboot
```

Open a new terminal afterwards so `jumpboot` and `jmp` are picked up.

> **Note:** the Windows executables are built with PyInstaller, which some antivirus tools flag as suspicious. This is a known false-positive pattern. If Defender complains, the source code in this repo is what the executables are built from.

### Linux (apt)

```
curl -fsSL https://kushchandak.github.io/jumpboot-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/jumpboot.gpg

echo "deb [signed-by=/usr/share/keyrings/jumpboot.gpg] https://kushchandak.github.io/jumpboot-repo stable main" | sudo tee /etc/apt/sources.list.d/jumpboot.list

sudo apt update
sudo apt install python3-jumpboot
```

The package is called `python3-jumpboot`, but the commands you type are still `jumpboot` and `jmp`.

## Usage

| Command | What it does |
| --- | --- |
| `jumpboot create <name>` | Creates a new workflow file and opens it for editing |
| `jumpboot edit <name>` | Reopens an existing workflow for editing |
| `jumpboot list` | Lists all your workflows |
| `jmp <name>` | Runs a workflow |

### Example

```
jumpboot create tryhackme
```

This creates a template file and opens it in Notepad (Windows) or nano (Linux). Fill it in, save, close, then run it:

```
jmp tryhackme
```

## Workflow files

Workflows are plain [TOML](https://toml.io) files stored in `~/.jumpboot/workflows/` (for example `C:\Users\<you>\.jumpboot\workflows\` on Windows).

```toml
name = "tryhackme"

# Websites to open. Include https:// or http://
urls = [
    "https://tryhackme.com",
    "https://docs.google.com/document/d/your-doc-id"
]

# Apps to open
apps = [
    "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
]
```

### About `apps`

- If an app is on your system PATH, its name is enough (for example `"firefox"` on most Linux systems).
- Otherwise, use the full path to the executable. On Windows, most apps (Chrome, Discord, and so on) are **not** on PATH, so you'll need the full `.exe` path.
- Windows Store (UWP) apps, like WhatsApp Desktop, aren't supported yet.

## Build from source

Requires Python 3.11+.

```
git clone https://github.com/KushChandak/jumpboot.git
cd jumpboot
pip install .
```

## Roadmap

- App name resolver, so workflows don't need full paths
- Support for Windows Store apps
- Optional startup trigger
- Record mode: save what you open during a session as a workflow

## License

MIT
