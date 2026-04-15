import sys

from micro_design_project.cli import main


if __name__ == "__main__":
    main(["benchmark", *sys.argv[1:]])
