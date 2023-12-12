from os import getenv
from typing import List
from random import choice
from typing import Dict
from typing import Any
from aiohttp import ClientSession

from discord import Intents
from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import has_role
from discord.utils import setup_logging
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

logger = get_logger()
setup_logging()

##
# Game CRUD
##

@typechecked
async def api_games(rest_key:str) -> List[Dict[str, Any]]:
    url = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game?select=*'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to get games. HTTP status code: {response.status}")

@typechecked
async def api_game(rest_key:str, name:str) -> List[Dict[str, Any]]:
    encoded_name = quote(name)
    url = f'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game?name=eq.{encoded_name}&select=*'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to get game. HTTP status code: {response.status}")

@typechecked
async def api_create_game(rest_key:str, name:str) -> List[Dict[str, Any]]:
    url = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    data = {
        'name': name,
    }
    async with ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 201:
                created_game = await response.json()
                return created_game
            else:
                raise Exception(f"Failed to create game. HTTP status code: {response.status}")

from urllib.parse import quote

@typechecked
async def api_delete_game(rest_key:str, name:str) -> List[Dict[str, Any]]:
    encoded_name = quote(name)
    url = f'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game?name=eq.{encoded_name}'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    async with ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                deleted_game = await response.json()
                return deleted_game
            else:
                raise Exception(f"Failed to delete game. HTTP status code: {response.status}")

##
# User CRUD
##

@typechecked
async def api_users(rest_key:str) -> List[Dict[str, Any]]:
    url = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user?select=*'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to get users. HTTP status code: {response.status}")

@typechecked
async def api_user(rest_key:str, name:str) -> List[Dict[str, Any]]:
    encoded_name = quote(name)
    url = f'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user?name=eq.{encoded_name}&select=*'
    headers = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to get user. HTTP status code: {response.status}")

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
    #games_list:List[Dict[str,Any]] = []

    
    @bot.event
    @typechecked
    async def on_ready()->None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)
        # TODO get list of games from rest api
        #global games_list
        #await logger.ainfo('on_ready() get the games list')
        #games_list = await api_games(rest_key)
        #await logger.ainfo('on_ready() games list: %s', games_list)
    # TODO admin command to reload list of games
    #@tasks.loop(seconds=600.0)
    #async def update_games(self):


    @bot.event
    @typechecked
    async def on_command_error(ctx, error:Exception)->None:
        """
        send a FYEO to the user and log the exception
        """

        if isinstance(error, CheckFailure):
            await ctx.send(error, ephemeral=True)
        await logger.aexception(error)


    @bot.command(name='shutdown')
    @has_role('admin')
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

    @has_role('admin')
    @bot.command(name='create_game')
    async def create_game(ctx)->None:
        name: str = ctx.message.content.split(maxsplit=1)[1] # Extract the name from the command message
        if name:
            await ctx.send(f"Creating game {name}", ephemeral=True)
            created_game = await api_create_game(rest_key, name)
            await ctx.send(f"Game '{created_game['name']}' created with ID {created_game['id']}!")
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @has_role('admin')
    @bot.command(name='delete_game')
    async def delete_game(ctx)->None:
        name: str = ctx.message.content.split(maxsplit=1)[1] # Extract the name from the command message
        if name:
            await ctx.send(f"Deleting game {name}", ephemeral=True)
            deleted_game = await api_delete_game(rest_key, name)
            await ctx.send(f"Game '{deleted_game['name']}' deleted with ID {deleted_game['id']}!")
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @has_role('admin')
    @bot.command(name='game')
    async def game(ctx)->None:
        name: str = ctx.message.content.split(maxsplit=1)[1] # Extract the name from the command message
        if name:
            await ctx.send(f"Getting game {name}", ephemeral=True)
            my_game = await api_game(rest_key, name)
            await ctx.send(f"Game '{my_game['name']}' with ID {my_game['id']}!")
        else:
            await ctx.send("Please provide a name for the game.", ephemeral=True)

    @bot.command(name='games')
    @typechecked
    async def games(ctx)->None:

        # TODO get list of games of rest api
        # TODO add one button per game

        await ctx.send('Getting games list', ephemeral=True)
        games_list:List[Dict[str,Any]] = await api_games(rest_key)

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

    return await bot.start(token)

    ##
    # User CRUD
    ##

    @has_role('admin')
    @bot.command(name='users')
    @typechecked
    async def users(ctx)->None:

        # TODO get list of users of rest api
        # TODO add one button per user

        await ctx.send('Getting users list', ephemeral=True)
        users_list:List[Dict[str,Any]] = await api_users(rest_key)

        #global users_list
        for user in users_list:
            await logger.ainfo('user: %s', user)
            await ctx.send(f'user: {user}', ephemeral=True)

    @has_role('admin')
    @bot.command(name='user')
    async def user(ctx)->None:
        name: str = ctx.message.content.split(maxsplit=1)[1] # Extract the name from the command message
        if name:
            await ctx.send(f"Getting user {name}", ephemeral=True)
            my_user = await api_user(rest_key, name)
            await ctx.send(f"Game '{my_user['name']}' with ID {my_user['id']}!")
        else:
            await ctx.send("Please provide a name for the user.", ephemeral=True)

##
# Simple
##

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
