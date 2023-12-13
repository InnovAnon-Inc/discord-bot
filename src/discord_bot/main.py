""" Application entrypoint """

from os import getenv

from structlog import get_logger
from typeguard import typechecked

from .bot import botze
from .hello import hellomain
from .log import logerror, trace

logger = get_logger()


@logerror(logger)
@trace(logger)
@hellomain(logger)
@typechecked
async def main() -> None:
    """
    read config vars from env and start the bot
    """

    token: str = getenv('DISCORD_TOKEN')
    guild: str = getenv('DISCORD_GUILD')
    restk: str = getenv('SUPABASE_KEY')
    return await botze(token, guild, restk)
