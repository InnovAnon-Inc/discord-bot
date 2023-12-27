"""
this file enables the program to be run by:

`python -m <module> [args]...`
"""

from asyncio import run

from .main import main

if __name__ == '__main__':
    run(main())

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
