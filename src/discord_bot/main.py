from os import getenv
from typing import List
from random import choice

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

@typechecked
class Buttons(View):
    @typechecked
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

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

    
    @bot.event
    @typechecked
    async def on_ready()->None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)
        # TODO get list of games from rest api
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

    @bot.command(name='games')
    @typechecked
    async def games(ctx)->None:

        # TODO get list of games of rest api
        # TODO add one button per game

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

    @typechecked
    async def get_games() -> List[Dict[str, Any]]:
        url = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/game?select=*'
        headers = {
            'apikey': 'YOUR_API_KEY',
            'Authorization': 'Bearer YOUR_AUTH_TOKEN'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Failed to get games. HTTP status code: {response.status}")

    @bot.event
    @typechecked
    async def on_ready() -> None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)
        games = await get_games()


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
