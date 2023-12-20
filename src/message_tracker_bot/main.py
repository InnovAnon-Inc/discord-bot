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

    token: str = getenv('DISCORD_TOKEN')
    guild: str = getenv('DISCORD_GUILD')
    restk: str = getenv('SUPABASE_KEY')
    chann: str = getenv('DISCORD_CHANNEL')
    invite_tracker_id:str = getenv('INVITE_TRACKER_ID')
    print(f'invite_tracker_id: {invite_tracker_id}')
    return await botze(token, guild, restk, chann, int(invite_tracker_id))
