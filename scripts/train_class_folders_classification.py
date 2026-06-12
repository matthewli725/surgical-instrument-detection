import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["train-class-folders-classification", *sys.argv[1:]])
