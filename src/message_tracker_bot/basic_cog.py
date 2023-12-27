""" Basic commands """

from typing import List, Union

from discord import ButtonStyle#, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ui import Button, View
from discord.ext.commands import command
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked
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
from .util import get_arg, get_args, get_discord_username, send_one_message
from .view import Buttons
from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *
from .view import Buttons

logger = get_logger()


@typechecked
class BasicCog(Cog):
    """ Basic-related commands """

    @typechecked
    def __init__(self, bot:Bot):
        self.bot      = bot


    #@bot.event
    @Cog.listener()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_command_error(self, ctx:Context, error: Exception) -> None:
        """
        send a FYEO to the user and log the exception
        """

        # default message should not leak sensitive data to hackers
        message: Union[str,
                       Exception] = 'Check the logs for a more detailed error description'

        # inform user of insufficient privileges
        if isinstance(error, CheckFailure):
            message = error

        # admins can see the error anyway
        elif await is_admin(ctx):
            message = error

        await ctx.send(message, ephemeral=True)
        if isinstance(error, Exception):
            await logger.aexception(error)
        else:
            await logger.aerror('Some error: %s', error)

    @has_role('admin')
    @command(name='shutdown')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def shutdown(self, ctx:Context) -> None:
        """
        Gracefully terminate the bot.

        see run.sh
        """

        await ctx.send('Disconnecting bot')
        return await self.bot.close()

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
