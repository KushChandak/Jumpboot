import argparse
from jumpboot.jumpboot import run_workflow


def main():
    parser = argparse.ArgumentParser(prog="jmp.py")
    parser.add_argument("workflow", help="workflow to run")

    args = parser.parse_args()

    run_workflow(args.workflow)


if __name__ == "__main__":
    main()
