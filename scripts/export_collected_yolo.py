import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["export-yolo", *sys.argv[1:]])
