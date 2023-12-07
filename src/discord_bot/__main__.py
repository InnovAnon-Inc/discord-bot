"""
this file enables the program to be run by:

`python -m <module> [args]...`
"""

from asyncio import run

from .main import main

if __name__ == '__main__':
    run(main())
