import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["train-class-folders-detection", *sys.argv[1:]])
