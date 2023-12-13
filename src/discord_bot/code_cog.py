""" Code commands """

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
class CodeCog(Cog):
    """ Code-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str):
        self.bot      = bot
        self.rest_key = rest_key

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_codes(self, ctx) -> None:
        """ Retrieve the all codes' names """

        # TODO get list of codes of rest api
        # TODO add one button per code

        await ctx.send('Getting codes list', ephemeral=True)
        codes_list: JSON= await api_get_codes(self.rest_key)

        # global codes_list
        # TODO just send one message
        for code in codes_list:
            await logger.ainfo('code: %s', code)
            user, game, secret = code
            await logger.ainfo('user: %s', user)
            await logger.ainfo('game: %s', game)
            await logger.ainfo('secret: %s', secret)
            await ctx.send(f'code: {code}', ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_code(self, ctx) -> None:
        """ <name>: Retrieve the `code` with the specified `user name` and `game name` """

        name, game = await get_args(ctx, 2)
        if not name or not game:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        await ctx.send(f"Getting code {name} {game}", ephemeral=True)
        my_code: JSON = await api_get_code(self.rest_key, name, game)
        # TODO unused codes, invite count
        await ctx.send(f"Code '{my_code['secret']}' with ID {my_code['user_id']} {my_code['game_id']}!")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_code(self, ctx) -> None:
        """ <name>: Register a `code` with the specified `user name`, `game name` and `secret` """

        name, game, secret = await get_args(ctx, 3)
        if not name or not game:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        await ctx.send(f"Creating code {name} {game}", ephemeral=True)
        created_code: str = await api_create_code(self.rest_key, name, game, secret)
        # await ctx.send(f"Game '{created_code['name']}' created with ID {created_code['id']}!")
        await ctx.send(f"Code {created_code} created")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_code(self, ctx) -> None:
        """ <name>: Unregister the `code` with the specified `user name` and `game name` """

        name, game = await get_args(ctx, 2)
        if not name or not game:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        await ctx.send(f"Deleting code {name} {game}", ephemeral=True)
        deleted_code: str = await api_delete_code(self.rest_key, name, game)
        # await ctx.send(f"Game '{deleted_code['name']}' deleted with ID {deleted_code['id']}!")
        await ctx.send(f"Code {deleted_code} deleted")

    # TODO regenerate random
    #@has_role('admin')
    #@command()
    #@logerror(logger)
    #@trace(logger)
    #@typechecked
    #async def rename_code(self, ctx) -> None:
    #    """ <name> <new_name>: Rename the `code` from `name` to `new name` """

    #    name, new_name = await get_args(ctx, 2)
    #    if not name:
    #        await ctx.send("Please provide a name for the code.", ephemeral=True)
    #        return

    #    if not new_name:
    #        await ctx.send("Please provide a new name for the code.", ephemeral=True)
    #        return

    #    await ctx.send(f"Renaming code {name} to {new_name}", ephemeral=True)
    #    my_code: str = await api_rename_code(self.rest_key, name, new_name)
    #    await ctx.send(f"Code {my_code} updated", ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_code_remaining(self, ctx) -> None:
        """ <name>: Get the remaining for the `code` with `user name` and `game name` """

        name, game = await get_args(ctx, 2)
        if not name or not game:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        await ctx.send(f"Getting code {name} {game} remaining", ephemeral=True)
        my_code: int = await api_get_code_remaining(self.rest_key, name, game)
        # TODO unused codes, invite count
        await ctx.send(f"Code invite count {my_code}")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_code_secret(self, ctx) -> None:
        """ <name>: Get the secret for the `code` with `user name` and `game name` """

        name, game = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        await ctx.send(f"Getting code {name} {game} secret", ephemeral=True)
        my_code: str = await api_get_code_secret(self.rest_key, name, game)
        # TODO unused codes, invite count
        await ctx.send(f"Code secret {my_code}")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_code_remaining(self, ctx) -> None:
        """ <name> <remaining>: Set the remaining for the `code` with `user name` and `game name` """

        name, game, remaining = await get_args(ctx, 3)
        if not name:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        if not remaining:
            await ctx.send("Please provide a remaining for the code.", ephemeral=True)
            return

        await ctx.send(f"Setting code {name} {game} remaining to {remaining}", ephemeral=True)
        my_code: str = await api_set_code_remaining(self.rest_key, name, game, int(remaining))
        await ctx.send(f"Code {my_code} updated", ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_code_secret(self, ctx) -> None:
        """ <name> <secret>: Set the secret for the `code` with `user name` and `game name` """

        name, game, secret = await get_args(ctx, 3)
        if not name or not game:
            await ctx.send("Please provide a user name and game name for the code.", ephemeral=True)
            return

        if not secret:
            await ctx.send("Please provide an secret for the code.", ephemeral=True)
            return

        await ctx.send(f"Setting code {name} {game} secret to {secret}", ephemeral=True)
        my_code: str = await api_set_code_secret(self.rest_key, name, game, secret)
        await ctx.send(f"Code {my_code} updated", ephemeral=True)

