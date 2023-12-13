""" Badge commands """

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
class BadgeCog(Cog):
    """ Badge-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str):
        self.bot      = bot
        self.rest_key = rest_key


    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_badge(self, ctx) -> None:
        """ <name>: Register a `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Creating badge {name}", ephemeral=True)
        created_badge: str = await api_create_badge(self.rest_key, name)
        # await ctx.send(f"Badge '{created_badge['name']}' created with ID {created_badge['id']}!")
        await ctx.send(f"Badge {created_badge} created")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_badge(self, ctx) -> None:
        """ <name>: Unregister the `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Deleting badge {name}", ephemeral=True)
        deleted_badge: str = await api_delete_badge(self.rest_key, name)
        # await ctx.send(f"Badge '{deleted_badge['name']}' deleted with ID {deleted_badge['id']}!")
        await ctx.send(f"Badge {deleted_badge} deleted")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_badge(self, ctx) -> None:
        """ <name>: Retrieve the `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Getting badge {name}", ephemeral=True)
        my_badge: JSON = await api_get_badge(self.rest_key, name)
        await ctx.send(f"Badge '{my_badge['name']}' with ID {my_badge['id']}!", ephemeral=True)

    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_badges(self, ctx) -> None:
        """ Retrieve the all badges' names """

        # TODO get list of badges of rest api
        # TODO add one button per badge

        await ctx.send('Getting badges list', ephemeral=True)
        badges_list: List[str] = await api_get_badges(self.rest_key)

        # global badges_list
        # TODO just send one message
        for badge in badges_list:
            await logger.ainfo('badge: %s', badge)
            await ctx.send(f'badge: {badge}', ephemeral=True)
        # assert(badges_list)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_badge(self, ctx) -> None:
        """ <name> <new_name>: Rename the `badge` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Renaming badge {name} to {new_name}", ephemeral=True)
        my_badge: str = await api_rename_badge(self.rest_key, name, new_name)
        await ctx.send(f"Badge {my_badge} updated", ephemeral=True)

