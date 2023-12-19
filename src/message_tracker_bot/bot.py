""" The bot proper """

from typing import List, Union

from discord import ButtonStyle, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ext.commands.errors import CheckFailure
from discord.ui import Button, View
from discord.utils import setup_logging
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked

from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *

logger = get_logger()
setup_logging()


# TODO invite tracker
#invites = {}
#last = ""

##
# 0xPepesPlay Bot
##

@typechecked
class UnfilteredBot(Bot):
    """An overridden version of the Bot class that will listen to other bots."""

    @logerror(logger)
    @trace(logger)
    @typechecked
    async def process_commands(self, message):
        """Override process_commands to listen to bots."""
        ctx:Context = await self.get_context(message)
        await self.invoke(ctx)


@logerror(logger)
@trace(logger)
@typechecked
async def botze(token: str, guild: str, rest_key: str, channel:str, invite_tracker_id:str) -> None:
    """
    scans for messages from InviteTracker
    and interacts with the REST API
    """

    intents: Intents = Intents.default()
    #intents.members = True
    # allow to get commands from GC
    intents.message_content = True  # v2
    # ChatGPT:
    # Change the type of bot from discord.ext.commands.Bot to discord.ext.commands.Bot.
    # This ensures that the event loop is properly managed by the commands.Bot class.
    bot: Bot = UnfilteredBot(intents=intents, command_prefix='?')
    # games_list:JSON = []


    await bot.add_cog(  BasicCog(bot))
    await bot.add_cog(   TestCog(bot, rest_key, guild, channel))
    await bot.add_cog(MessageCog(bot, rest_key, invite_tracker_id))


    return await bot.start(token)

