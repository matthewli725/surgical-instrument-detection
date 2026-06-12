import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["auto-annotate-class-folders", *sys.argv[1:]])
