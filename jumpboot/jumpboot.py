import os
import webbrowser
import subprocess
import argparse
import platform
import tomllib
from pathlib import Path
import re

TEMPLATE = r'''# ============================================
# Jumpboot Workflow: {name}
# ============================================
# Add as many URLs or apps as you want below.
# Just add a new line inside the [ ] brackets,
# separated by commas.

name = "{name}"

# ---- Websites / links to open ----
# Include https:// or http:// in the url
# Example: "https://youtube.com/watch?v=xyz"
# Enclose URL in "". For Multiple URLs, put , inbetween. 
urls = [

]

# ---- Apps to open ----
# Use the full path to the app's .exe
# (backslashes are fine, no need to escape them)
# Example: "C:\Program Files\Notepad++\notepad++.exe"
# Enclose Path in "". For Multiple Paths, put , inbetween
apps = [

]
'''
WORKFLOW_DIR = Path.home() / ".jumpboot" / "workflows"

def run_workflow(name):

    try:
        workflow_path = WORKFLOW_DIR / f"{name}.toml"

        # Read TOML as text first so Windows backslashes
        # don't break TOML parsing.
        with open(workflow_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Convert backslashes to forward slashes inside apps
        apps_match = re.search(r'(?ms)^apps\s*=\s*\[(.*?)\]', content)

        if apps_match:
            apps_content = apps_match.group(1)
            apps_content = apps_content.replace("\\", "/")

            content = (
                content[:apps_match.start(1)]
                + apps_content
                + content[apps_match.end(1):]
            )

        try:
            data = tomllib.loads(content)

            for url in data.get("urls", []):
                webbrowser.open(url, new=0)

            for app in data.get("apps", []):
                try:
                    app_path = app.replace("\\", "/")
                    subprocess.Popen([app_path])

                except FileNotFoundError:
                    print("Not a Valid App Location")

        except tomllib.TOMLDecodeError:
            print("Check your TOML config file! You Maybe Forgot Something")

    except FileNotFoundError:
        print("Workflow Not Found")

def create_workflow(name):
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    path = WORKFLOW_DIR / f"{name}.toml"

    if path.exists():
        print(f"Workflow '{name}' already exists at {path}")
    else:
        content = TEMPLATE.format(name=name)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created {path}")

    if platform.system() == "Windows":
        subprocess.run(["notepad", path])
    else:
        subprocess.run(["nano", path])

def edit_workflow(workflow):
    path = WORKFLOW_DIR / f"{workflow}.toml"

    if not path.is_file():
        print("Workflow Not Found")
        return

    if platform.system() == "Windows":
        subprocess.run(["notepad", str(path)])
    else:
        subprocess.run(["nano", str(path)])

def jumpboot():
    parser = argparse.ArgumentParser(prog="jumpboot")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="creates a workflow")
    create_parser.add_argument("name", help="name of new workflow")

    edit_parser = subparsers.add_parser("edit", help="edit workflow")
    edit_parser.add_argument("workflow", help="workflow")

    list_parser = subparsers.add_parser("list", help="lists all available workflows")
    args = parser.parse_args()

    if args.command == "create":
        create_workflow(args.name)

    elif args.command == "edit":
        edit_workflow(args.workflow)

    elif args.command == "list":
        try:
            workflows = [
                item for item in WORKFLOW_DIR.iterdir()
                if item.is_file() and item.suffix == ".toml"
            ]

            if not workflows:
                print("No Workflows Found")
            else:
                for item in workflows:
                    print(item.stem)

        except FileNotFoundError:
            print("No Workflows Found")


if __name__ == "__main__":
    jumpboot()










