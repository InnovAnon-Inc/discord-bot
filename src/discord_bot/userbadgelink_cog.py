""" UserBadgeLink commands """

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
class UserBadgeLinkCog(Cog):
    """ UserBadgeLink-related commands """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str):
        self.bot      = bot
        self.rest_key = rest_key

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_userbadgelinks(self, ctx) -> None:
        """ Retrieve the all userbadgelinks' names """

        # TODO get list of userbadgelinks of rest api
        # TODO add one button per userbadgelink

        await ctx.send('Getting userbadgelinks list', ephemeral=True)
        userbadgelinks_list: JSON= await api_get_userbadgelinks(self.rest_key)

        # global userbadgelinks_list
        # TODO just send one message
        for userbadgelink in userbadgelinks_list:
            await logger.ainfo('userbadgelink: %s', userbadgelink)
            user, badge = userbadgelink
            await logger.ainfo('user: %s', user)
            await logger.ainfo('badge: %s', badge)
            await ctx.send(f'userbadgelink: {userbadgelink}', ephemeral=True)

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_userbadgelink(self, ctx) -> None:
        """ <name>: Retrieve the `userbadgelink` with the specified `user name` and `badge name` """

        name, badge = await get_args(ctx, 2)
        if not name or not badge:
            await ctx.send("Please provide a user name and badge name for the userbadgelink.", ephemeral=True)
            return

        await ctx.send(f"Getting userbadgelink {name} {badge}", ephemeral=True)
        my_userbadgelink: JSON = await api_get_userbadgelink(self.rest_key, name, badge)
        # TODO unused userbadgelinks, invite count
        await ctx.send(f"UserBadgeLink with ID {my_userbadgelink['user_id']} {my_userbadgelink['badge_id']}!")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_userbadgelink(self, ctx) -> None:
        """ <name>: Register a `userbadgelink` with the specified `user name` and `badge name` """

        name, badge = await get_args(ctx, 2)
        if not name or not badge:
            await ctx.send("Please provide a user name and badge name for the userbadgelink.", ephemeral=True)
            return

        await ctx.send(f"Creating userbadgelink {name} {badge}", ephemeral=True)
        created_userbadgelink: str = await api_create_userbadgelink(self.rest_key, name, badge)
        # await ctx.send(f"Badge '{created_userbadgelink['name']}' created with ID {created_userbadgelink['id']}!")
        await ctx.send(f"UserBadgeLink {created_userbadgelink} created")

    @has_role('admin')
    @command()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_userbadgelink(self, ctx) -> None:
        """ <name>: Unregister the `userbadgelink` with the specified `user name` and `badge name` """

        name, badge = await get_args(ctx, 2)
        if not name or not badge:
            await ctx.send("Please provide a user name and badge name for the userbadgelink.", ephemeral=True)
            return

        await ctx.send(f"Deleting userbadgelink {name} {badge}", ephemeral=True)
        deleted_userbadgelink: str = await api_delete_userbadgelink(self.rest_key, name, badge)
        # await ctx.send(f"Badge '{deleted_userbadgelink['name']}' deleted with ID {deleted_userbadgelink['id']}!")
        await ctx.send(f"UserBadgeLink {deleted_userbadgelink} deleted")

