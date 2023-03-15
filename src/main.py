#!/usr/bin/env python

import os
from clize import run


def main():

    """Triggers Pipeline"""

    os.system("dvc repro")

    return


if __name__ == "__main__":
    run(main)
