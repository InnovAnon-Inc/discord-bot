""" Application entrypoint """

from os import getenv

from structlog import get_logger
from typeguard import typechecked

from .bot import botze
from .hello import hellomain, hellodiscord
from .log import logerror, trace

logger = get_logger()


@logerror(logger)
@trace(logger)
@hellomain(logger)
@hellodiscord(logger)
@typechecked
async def main() -> None:
    """
    read config vars from env and start the bot
    """

    token            :str =     getenv('DISCORD_TOKEN')
    guild            :str =     getenv('DISCORD_GUILD')
    restk            :str =     getenv('SUPABASE_KEY')
    chann            :int = int(getenv('DISCORD_CHANNEL'))
    invite_tracker_id:int = int(getenv('INVITE_TRACKER_ID'))
    print(f'invite_tracker_id: {invite_tracker_id}')
    return await botze(token, guild, restk, chann, invite_tracker_id)

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
