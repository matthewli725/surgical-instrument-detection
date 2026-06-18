import sys

from trayguard.cli import main


if __name__ == "__main__":
    main(["benchmark", *sys.argv[1:]])
