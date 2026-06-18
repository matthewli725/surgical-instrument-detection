import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["collect-class-folder", *sys.argv[1:]])
