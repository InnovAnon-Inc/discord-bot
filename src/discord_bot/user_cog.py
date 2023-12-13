""" User commands """

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
class UserCog(Cog):
    """ User-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str):
        self.bot      = bot
        self.rest_key = rest_key

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_users(self, ctx) -> None:
        """ Retrieve the all users' names """

        # TODO get list of users of rest api
        # TODO add one button per user

        await ctx.send('Getting users list', ephemeral=True)
        users_list: List[str] = await api_get_users(self.rest_key)

        # global users_list
        # TODO just send one message
        for user in users_list:
            await logger.ainfo('user: %s', user)
            await ctx.send(f'user: {user}', ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user(self, ctx) -> None:
        """ <name>: Retrieve the `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name}", ephemeral=True)
        my_user: JSON = await api_get_user(self.rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User '{my_user['name']}' with ID {my_user['id']}!")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_user(self, ctx) -> None:
        """ <name>: Register a `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Creating user {name}", ephemeral=True)
        created_user: str = await api_create_user(self.rest_key, name)
        # await ctx.send(f"Game '{created_user['name']}' created with ID {created_user['id']}!")
        await ctx.send(f"User {created_user} created")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_user(self, ctx) -> None:
        """ <name>: Unregister the `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Deleting user {name}", ephemeral=True)
        deleted_user: str = await api_delete_user(self.rest_key, name)
        # await ctx.send(f"Game '{deleted_user['name']}' deleted with ID {deleted_user['id']}!")
        await ctx.send(f"User {deleted_user} deleted")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_user(self, ctx) -> None:
        """ <name> <new_name>: Rename the `user` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the user.", ephemeral=True)
            return

        await ctx.send(f"Renaming user {name} to {new_name}", ephemeral=True)
        my_user: str = await api_rename_user(self.rest_key, name, new_name)
        await ctx.send(f"User {my_user} updated", ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user_invite_count(self, ctx) -> None:
        """ <name>: Get the invite count for the `user` with `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name} invite count", ephemeral=True)
        my_user: int = await api_get_user_invite_count(self.rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User invite count {my_user}")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user_unclaimed_codes(self, ctx) -> None:
        """ <name>: Get the unclaimed codes for the `user` with `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name} unclaimed codes", ephemeral=True)
        my_user: int = await api_get_user_unclaimed_codes(self.rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User unclaimed codes {my_user}")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_user_invite_count(self, ctx) -> None:
        """ <name> <invite_count>: Set the invite count for the `user` with `name` """

        name, invite_count = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not invite_count:
            await ctx.send("Please provide an invite count for the user.", ephemeral=True)
            return

        await ctx.send(f"Setting user {name} invite count to {invite_count}", ephemeral=True)
        my_user: str = await api_set_user_invite_count(self.rest_key, name, int(invite_count))
        await ctx.send(f"User {my_user} updated", ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_user_unclaimed_codes(self, ctx) -> None:
        """ <name> <unclaimed_codes>: Set the unclaimed codes for the `user` with `name` """

        name, unclaimed_codes = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not unclaimed_codes:
            await ctx.send("Please provide an unclaimed codes for the user.", ephemeral=True)
            return

        await ctx.send(f"Setting user {name} unclaimed codes to {unclaimed_codes}", ephemeral=True)
        my_user: str = await api_set_user_unclaimed_codes(self.rest_key, name, int(unclaimed_codes))
        await ctx.send(f"User {my_user} updated", ephemeral=True)

