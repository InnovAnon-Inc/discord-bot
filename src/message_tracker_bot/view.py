""" The bot proper """

#from discord import ButtonStyle, Intents  # , Interaction, Member, Message
#from discord.ui import Button
from discord.ui import View
from structlog import get_logger
from typeguard import typechecked

from .types import P

logger = get_logger()


@typechecked
class Buttons(View):
    """ Buttons to display on command """

    @typechecked
    def __init__(self, *_:P.args, timeout:int=180):
        super().__init__(timeout=timeout)

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
