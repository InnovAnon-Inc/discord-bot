""" The bot proper """

from typing import List, Union

from discord import ButtonStyle, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role
from discord.ext.commands.errors import CheckFailure
from discord.ui import Button, View
from discord.utils import setup_logging
from structlog import get_logger
from typeguard import typechecked

from .crud import *
from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *
from .view import Buttons

logger = get_logger()
setup_logging()



##
# 0xPepesPlay Bot
##


@logerror(logger)
@trace(logger)
@typechecked
async def botze(token: str, guild: str, rest_key: str) -> None:
    """
    implements the business logic for the 0xpepesplay project
    by interacting with the REST API
    """

    intents: Intents = Intents.default()
    intents.members = True
    # allow to get commands from GC
    intents.message_content = True  # v2
    bot: Bot = Bot(intents=intents, command_prefix='!')
    # games_list:JSON = []

    @bot.event
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_ready() -> None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)
        # TODO get list of games from rest api
        # global games_list
        # await logger.ainfo('on_ready() get the games list')
        # games_list = await api_get_games(rest_key)
        # await logger.ainfo('on_ready() games list: %s', games_list)
    # TODO admin command to reload list of games
    # @tasks.loop(seconds=600.0)
    # async def update_games(self):

    @bot.event
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_command_error(ctx, error: Exception) -> None:
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
        await logger.aexception(error)

    @has_role('admin')
    @bot.command(name='shutdown')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def shutdown(ctx) -> None:
        """
        Gracefully terminate the bot.

        see run.sh
        """

        await ctx.send('Disconnecting bot')
        return await bot.close()

    ##
    # TODO
    ##

    # if invite count > 10
    # then grant Flight 69 badge
        """
        ```
        curl -X POST 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/userbadgelink' \
        -H "apikey: $SUPABASE_KEY" \
        -H "Authorization: Bearer $SUPABASE_KEY" \
        -H "Content-Type: application/json" \
        -H "Prefer: return=minimal" \
        -d '{ "some_column": "someValue", "other_column": "otherValue" }'

        ```
        """
    # if user has Flight 69 badge
        """
        ```
        curl 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/userbadgelink?select=user_id' \
        -H "apikey: $SUPABASE_KEY" \
        -H "Authorization: Bearer $SUPABASE_KEY"

        ```
        """
    # then grant shadow? role

    # TODO allow user to use `unused_codes` by incrementing `remaining`
    # TODO allow user to get and (re)generate `secret`
    # TODO maybe provide a direct link to play the game

    ##
    # Code CRUD
    ##

    ##
    # UserBadgeLink CRUD
    ##

    await bot.add_cog( GameCog(bot, rest_key))
    await bot.add_cog( UserCog(bot, rest_key))
    await bot.add_cog( CodeCog(bot, rest_key))
    await bot.add_cog(BadgeCog(bot, rest_key))
    return await bot.start(token)
