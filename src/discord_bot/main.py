from os import getenv
from typing import List
from random import choice
from typing import Dict
from typing import Any
from typing import Union
from aiohttp import ClientSession
from urllib.parse import urlencode

from discord import Intents
from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import has_role
from discord.utils import setup_logging
from discord.utils import get
from discord.utils import find
from discord.ui import Button
from discord import ButtonStyle
from discord import Interaction
from discord import Member
from discord.ui import View
from structlog import get_logger
from typeguard import typechecked
from discord.ext.commands.errors import CheckFailure

from .hello import hellomain
from .types import P
from .log import trace
from .log import logerror
from .crud import *
from .util import is_admin
from .util import get_arg
from .util import get_args
from .types import JSON
from .types import HEADERS
from .types import DATA
from .types import PARAMS

logger = get_logger()
setup_logging()

##
# Command View
##

@typechecked
class Buttons(View):
    @typechecked
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

##
# 0xPepesPlay Bot
##

@logerror(logger)
@trace(logger)
@typechecked
async def bot(token:str, guild:str, rest_key:str)->None:
    """
    implements the business logic for the 0xpepesplay project
    by interacting with the REST API
    """
    
    intents:Intents         = Intents.default()
    intents.members         = True
    # allow to get commands from GC
    intents.message_content = True #v2
    bot    :Bot             = Bot(intents=intents, command_prefix='!')
    #games_list:JSON = []

    
    @logerror(logger)
    @trace(logger)
    @bot.event
    @typechecked
    async def on_ready()->None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)
        # TODO get list of games from rest api
        #global games_list
        #await logger.ainfo('on_ready() get the games list')
        #games_list = await api_get_games(rest_key)
        #await logger.ainfo('on_ready() games list: %s', games_list)
    # TODO admin command to reload list of games
    #@tasks.loop(seconds=600.0)
    #async def update_games(self):


    @logerror(logger)
    @trace(logger)
    @bot.event
    @typechecked
    async def on_command_error(ctx, error:Exception)->None:
        """
        send a FYEO to the user and log the exception
        """

        # default message should not leak sensitive data to hackers
        message:Union[str,Exception] = 'Check the logs for a more detailed error description'

        # inform user of insufficient privileges
        if isinstance(error, CheckFailure):
            message = error

        # admins can see the error anyway
        elif await is_admin(ctx):
            message = error

        await ctx.send(message, ephemeral=True)
        await logger.aexception(error)


    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='shutdown')
    @typechecked
    async def shutdown(ctx)->None:
        """
        gracefully terminate the application.

        see run.sh
        """

        await ctx.send('Disconnecting bot')
        return await bot.close()

    ##
    # TODO
    ##

    # if invite count > 10
        """
        ```
        curl 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user?select=invite_count' \
        -H "apikey: $SUPABASE_KEY" \
        -H "Authorization: Bearer $SUPABASE_KEY"
        ```
        """
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

    # get list of games
        """
        ```
        curl 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game?select=*' \
        -H "apikey: $SUPABASE_KEY" \
        -H "Authorization: Bearer $SUPABASE_KEY"
        ```
        """
    # TODO allow user to use `unused_codes` by incrementing `remaining`
    # TODO allow user to get and (re)generate `secret`
    # TODO maybe provide a direct link to play the game




    ##
    # Game CRUD
    ##

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='create_game')
    @typechecked
    async def create_game(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Creating game {name}", ephemeral=True)
            created_game:str = await api_create_game(rest_key, name)
            #await ctx.send(f"Game '{created_game['name']}' created with ID {created_game['id']}!")
            await ctx.send(f"Game {created_game} created")
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='delete_game')
    @typechecked
    async def delete_game(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Deleting game {name}", ephemeral=True)
            deleted_game:str = await api_delete_game(rest_key, name)
            #await ctx.send(f"Game '{deleted_game['name']}' deleted with ID {deleted_game['id']}!")
            await ctx.send(f"Game {deleted_game} deleted")
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='get_game')
    @typechecked
    async def get_game(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Getting game {name}", ephemeral=True)
            my_game:JSON = await api_get_game(rest_key, name)
            await ctx.send(f"Game '{my_game['name']}' with ID {my_game['id']}!", ephemeral=True)
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @bot.command(name='get_games')
    @typechecked
    async def get_games(ctx)->None:

        # TODO get list of games of rest api
        # TODO add one button per game

        await ctx.send('Getting games list', ephemeral=True)
        games_list:JSON = await api_get_games(rest_key)

        #global games_list
        for game in games_list:
            await logger.ainfo('game: %s', game)
            await ctx.send(f'game: {game}', ephemeral=True)
        #assert(games_list)

        view:View = Buttons()
        view.add_item(Button(label="URL Button",style=ButtonStyle.link,url="https://github.com/lykn"))
        await ctx.send("This message has buttons!",view=view)

        
        # TODO button callback function to get access code from rest api
        # TODO user id : #print(message.author.id)

        #brooklyn_99_quotes:List[str] = [
        #    'I\'m the human form of the 💯 emoji.',
        #    'Bingpot!',
        #    (
        #        'Cool. Cool cool cool cool cool cool cool, '
        #        'no doubt no doubt no doubt no doubt.'
        #    ),
        #]

        #response:str = choice(brooklyn_99_quotes)
        #print(message.author.id)
        #response = f'FYI({message.author.id}): {response}'
        #await ctx.send(response, ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='rename_game')
    @typechecked
    async def rename_game(ctx)->None:
        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return
        if not new_name:
            await ctx.send("Please provide a new name for the game.", ephemeral=True)
            return
        await ctx.send(f"Renaming game {name} to {new_name}", ephemeral=True)
        my_game:str = await api_rename_game(rest_key, name, new_name)
        await ctx.send(f"Game {my_game} updated", ephemeral=True)


    ##
    # User CRUD
    ##

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='get_users')
    @typechecked
    async def get_users(ctx)->None:

        # TODO get list of users of rest api
        # TODO add one button per user

        await ctx.send('Getting users list', ephemeral=True)
        users_list:JSON = await api_get_users(rest_key)

        #global users_list
        for user in users_list:
            await logger.ainfo('user: %s', user)
            await ctx.send(f'user: {user}', ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='get_user')
    @typechecked
    async def get_user(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Getting user {name}", ephemeral=True)
            my_user:JSON = await api_get_user(rest_key, name)
            # TODO unused codes, invite count
            await ctx.send(f"User '{my_user['name']}' with ID {my_user['id']}!")
        else:
            await ctx.send("Please provide a name for the user.", ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='create_user')
    @typechecked
    async def create_user(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Creating user {name}", ephemeral=True)
            created_user:str = await api_create_user(rest_key, name)
            #await ctx.send(f"Game '{created_user['name']}' created with ID {created_user['id']}!")
            await ctx.send(f"User {created_user} created")
        else:
            await ctx.send("Please provide a name for the user.", ephemeral=True)

    @logerror(logger)
    @trace(logger)
    @has_role('admin')
    @bot.command(name='delete_user')
    @typechecked
    async def delete_user(ctx)->None:
        name:str = await get_arg(ctx)
        if name:
            await ctx.send(f"Deleting user {name}", ephemeral=True)
            deleted_user:str = await api_delete_user(rest_key, name)
            #await ctx.send(f"Game '{deleted_user['name']}' deleted with ID {deleted_user['id']}!")
            await ctx.send(f"User {deleted_user} deleted")
        else:
            await ctx.send("Please provide a name for the user.", ephemeral=True)

    return await bot.start(token)


##
# Simple
##

@logerror(logger)
@trace(logger)
@hellomain(logger)
@typechecked
async def main()->None:
    """
    read config vars from env and start the bot
    """

    TOKEN:str = getenv('DISCORD_TOKEN')
    GUILD:str = getenv('DISCORD_GUILD')
    RESTK:str = getenv('SUPABASE_KEY')
    return await bot(TOKEN, GUILD, RESTK)
