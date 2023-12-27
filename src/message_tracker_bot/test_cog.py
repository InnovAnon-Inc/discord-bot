""" Test commands """

from typing import List

from discord import ButtonStyle#, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ui import Button, View
from discord.ext.commands import command
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked

from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, get_discord_username, send_one_message
from .view import Buttons

logger = get_logger()


@typechecked
class TestCog(Cog):
    """ Test-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str, guild:str, channel:int):
        self.bot      = bot
        self.rest_key = rest_key
        self.guild    = guild
        self.channel  = channel

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def do_test(self, ctx:Context) -> None:
        await logger.ainfo("guild: %s", self.guild)
        await ctx.send(f'guild: {self.guild}', ephemeral=True)
        
        await logger.ainfo("channel: %s", self.channel)
        await ctx.send(f'channel: {self.channel}', ephemeral=True)



__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
