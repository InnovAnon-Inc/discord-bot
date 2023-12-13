""" Game commands """

from typing import List

from discord import ButtonStyle#, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role
from discord.ui import Button, View
from discord.ext.commands import command
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked

from .crud import *
from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args
from .view import Buttons

logger = get_logger()


@typechecked
class GameCog(Cog):
    """ Game-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str):
        self.bot      = bot
        self.rest_key = rest_key

    @has_role('admin')
    @command()#name='create_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_game(self, ctx) -> None:
        """ <name>: Register a `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Creating game {name}", ephemeral=True)
        created_game: str = await api_create_game(self.rest_key, name)
        # await ctx.send(f"Game '{created_game['name']}' created with ID {created_game['id']}!")
        await ctx.send(f"Game {created_game} created")

    @has_role('admin')
    @command()#name='delete_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_game(self, ctx) -> None:
        """ <name>: Unregister the `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Deleting game {name}", ephemeral=True)
        deleted_game: str = await api_delete_game(self.rest_key, name)
        # await ctx.send(f"Game '{deleted_game['name']}' deleted with ID {deleted_game['id']}!")
        await ctx.send(f"Game {deleted_game} deleted")

    @has_role('admin')
    @command()#name='get_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_game(self, ctx) -> None:
        """ <name>: Retrieve the `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Getting game {name}", ephemeral=True)
        my_game: JSON = await api_get_game(self.rest_key, name)
        await ctx.send(f"Game '{my_game['name']}' with ID {my_game['id']}!", ephemeral=True)

    @command()#name='get_games')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_games(self, ctx) -> None:
        """ Retrieve the all games' names """

        # TODO get list of games of rest api
        # TODO add one button per game

        await ctx.send('Getting games list', ephemeral=True)
        games_list: List[str] = await api_get_games(self.rest_key)

        # global games_list
        # TODO just send one message
        for game in games_list:
            await logger.ainfo('game: %s', game)
            await ctx.send(f'game: {game}', ephemeral=True)
        # assert(games_list)

        view: View = Buttons()
        view.add_item(Button(label="URL Button",
                      style=ButtonStyle.link, url="https://github.com/lykn"))
        await ctx.send("This message has buttons!", view=view)

        # TODO button callback function to get access code from rest api
        # TODO user id : #print(message.author.id)

        # brooklyn_99_quotes:List[str] = [
        #    'I\'m the human form of the 💯 emoji.',
        #    'Bingpot!',
        #    (
        #        'Cool. Cool cool cool cool cool cool cool, '
        #        'no doubt no doubt no doubt no doubt.'
        #    ),
        # ]

        # response:str = choice(brooklyn_99_quotes)
        # print(message.author.id)
        # response = f'FYI({message.author.id}): {response}'
        # await ctx.send(response, ephemeral=True)

    @has_role('admin')
    @command()#name='rename_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_game(self, ctx) -> None:
        """ <name> <new_name>: Rename the `game` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the game.", ephemeral=True)
            return

        await ctx.send(f"Renaming game {name} to {new_name}", ephemeral=True)
        my_game: str = await api_rename_game(self.rest_key, name, new_name)
        await ctx.send(f"Game {my_game} updated", ephemeral=True)

