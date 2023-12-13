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
#from .cogs import *
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
    # Game CRUD
    ##

    @has_role('admin')
    @bot.command(name='create_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_game(ctx) -> None:
        """ <name>: Register a `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Creating game {name}", ephemeral=True)
        created_game: str = await api_create_game(rest_key, name)
        # await ctx.send(f"Game '{created_game['name']}' created with ID {created_game['id']}!")
        await ctx.send(f"Game {created_game} created")

    @has_role('admin')
    @bot.command(name='delete_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_game(ctx) -> None:
        """ <name>: Unregister the `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Deleting game {name}", ephemeral=True)
        deleted_game: str = await api_delete_game(rest_key, name)
        # await ctx.send(f"Game '{deleted_game['name']}' deleted with ID {deleted_game['id']}!")
        await ctx.send(f"Game {deleted_game} deleted")

    @has_role('admin')
    @bot.command(name='get_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_game(ctx) -> None:
        """ <name>: Retrieve the `game` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        await ctx.send(f"Getting game {name}", ephemeral=True)
        my_game: JSON = await api_get_game(rest_key, name)
        await ctx.send(f"Game '{my_game['name']}' with ID {my_game['id']}!", ephemeral=True)

    @bot.command(name='get_games')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_games(ctx) -> None:
        """ Retrieve the all games' names """

        # TODO get list of games of rest api
        # TODO add one button per game

        await ctx.send('Getting games list', ephemeral=True)
        games_list: List[str] = await api_get_games(rest_key)

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
    @bot.command(name='rename_game')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_game(ctx) -> None:
        """ <name> <new_name>: Rename the `game` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the game.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the game.", ephemeral=True)
            return

        await ctx.send(f"Renaming game {name} to {new_name}", ephemeral=True)
        my_game: str = await api_rename_game(rest_key, name, new_name)
        await ctx.send(f"Game {my_game} updated", ephemeral=True)

    ##
    # User CRUD
    ##

    @has_role('admin')
    @bot.command(name='get_users')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_users(ctx) -> None:
        """ Retrieve the all users' names """

        # TODO get list of users of rest api
        # TODO add one button per user

        await ctx.send('Getting users list', ephemeral=True)
        users_list: List[str] = await api_get_users(rest_key)

        # global users_list
        # TODO just send one message
        for user in users_list:
            await logger.ainfo('user: %s', user)
            await ctx.send(f'user: {user}', ephemeral=True)

    @has_role('admin')
    @bot.command(name='get_user')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user(ctx) -> None:
        """ <name>: Retrieve the `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name}", ephemeral=True)
        my_user: JSON = await api_get_user(rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User '{my_user['name']}' with ID {my_user['id']}!")

    @has_role('admin')
    @bot.command(name='create_user')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_user(ctx) -> None:
        """ <name>: Register a `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Creating user {name}", ephemeral=True)
        created_user: str = await api_create_user(rest_key, name)
        # await ctx.send(f"Game '{created_user['name']}' created with ID {created_user['id']}!")
        await ctx.send(f"User {created_user} created")

    @has_role('admin')
    @bot.command(name='delete_user')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_user(ctx) -> None:
        """ <name>: Unregister the `user` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Deleting user {name}", ephemeral=True)
        deleted_user: str = await api_delete_user(rest_key, name)
        # await ctx.send(f"Game '{deleted_user['name']}' deleted with ID {deleted_user['id']}!")
        await ctx.send(f"User {deleted_user} deleted")

    @has_role('admin')
    @bot.command(name='rename_user')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_user(ctx) -> None:
        """ <name> <new_name>: Rename the `user` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the user.", ephemeral=True)
            return

        await ctx.send(f"Renaming user {name} to {new_name}", ephemeral=True)
        my_user: str = await api_rename_user(rest_key, name, new_name)
        await ctx.send(f"User {my_user} updated", ephemeral=True)

    @has_role('admin')
    @bot.command(name='get_user_invite_count')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user_invite_count(ctx) -> None:
        """ <name>: Get the invite count for the `user` with `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name} invite count", ephemeral=True)
        my_user: int = await api_get_user_invite_count(rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User invite count {my_user}")

    @has_role('admin')
    @bot.command(name='get_user_unclaimed_codes')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_user_unclaimed_codes(ctx) -> None:
        """ <name>: Get the unclaimed codes for the `user` with `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        await ctx.send(f"Getting user {name} unclaimed codes", ephemeral=True)
        my_user: int = await api_get_user_unclaimed_codes(rest_key, name)
        # TODO unused codes, invite count
        await ctx.send(f"User unclaimed codes {my_user}")

    @has_role('admin')
    @bot.command(name='set_user_invite_count')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_user_invite_count(ctx) -> None:
        """ <name> <invite_count>: Set the invite count for the `user` with `name` """

        name, invite_count = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not invite_count:
            await ctx.send("Please provide an invite count for the user.", ephemeral=True)
            return

        await ctx.send(f"Setting user {name} invite count to {invite_count}", ephemeral=True)
        my_user: str = await api_set_user_invite_count(rest_key, name, int(invite_count))
        await ctx.send(f"User {my_user} updated", ephemeral=True)

    @has_role('admin')
    @bot.command(name='set_user_unclaimed_codes')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def set_user_unclaimed_codes(ctx) -> None:
        """ <name> <unclaimed_codes>: Set the unclaimed codes for the `user` with `name` """

        name, unclaimed_codes = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the user.", ephemeral=True)
            return

        if not unclaimed_codes:
            await ctx.send("Please provide an unclaimed codes for the user.", ephemeral=True)
            return

        await ctx.send(f"Setting user {name} unclaimed codes to {unclaimed_codes}", ephemeral=True)
        my_user: str = await api_set_user_unclaimed_codes(rest_key, name, int(unclaimed_codes))
        await ctx.send(f"User {my_user} updated", ephemeral=True)

    ##
    # Badge CRUD
    ##

    @has_role('admin')
    @bot.command(name='create_badge')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def create_badge(ctx) -> None:
        """ <name>: Register a `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Creating badge {name}", ephemeral=True)
        created_badge: str = await api_create_badge(rest_key, name)
        # await ctx.send(f"Badge '{created_badge['name']}' created with ID {created_badge['id']}!")
        await ctx.send(f"Badge {created_badge} created")

    @has_role('admin')
    @bot.command(name='delete_badge')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def delete_badge(ctx) -> None:
        """ <name>: Unregister the `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Deleting badge {name}", ephemeral=True)
        deleted_badge: str = await api_delete_badge(rest_key, name)
        # await ctx.send(f"Badge '{deleted_badge['name']}' deleted with ID {deleted_badge['id']}!")
        await ctx.send(f"Badge {deleted_badge} deleted")

    @has_role('admin')
    @bot.command(name='get_badge')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_badge(ctx) -> None:
        """ <name>: Retrieve the `badge` with the specified `name` """

        name: str = await get_arg(ctx)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Getting badge {name}", ephemeral=True)
        my_badge: JSON = await api_get_badge(rest_key, name)
        await ctx.send(f"Badge '{my_badge['name']}' with ID {my_badge['id']}!", ephemeral=True)

    @bot.command(name='get_badges')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def get_badges(ctx) -> None:
        """ Retrieve the all badges' names """

        # TODO get list of badges of rest api
        # TODO add one button per badge

        await ctx.send('Getting badges list', ephemeral=True)
        badges_list: List[str] = await api_get_badges(rest_key)

        # global badges_list
        # TODO just send one message
        for badge in badges_list:
            await logger.ainfo('badge: %s', badge)
            await ctx.send(f'badge: {badge}', ephemeral=True)
        # assert(badges_list)

    @has_role('admin')
    @bot.command(name='rename_badge')
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def rename_badge(ctx) -> None:
        """ <name> <new_name>: Rename the `badge` from `name` to `new name` """

        name, new_name = await get_args(ctx, 2)
        if not name:
            await ctx.send("Please provide a name for the badge.", ephemeral=True)
            return

        if not new_name:
            await ctx.send("Please provide a new name for the badge.", ephemeral=True)
            return

        await ctx.send(f"Renaming badge {name} to {new_name}", ephemeral=True)
        my_badge: str = await api_rename_badge(rest_key, name, new_name)
        await ctx.send(f"Badge {my_badge} updated", ephemeral=True)

    ##
    # Code CRUD
    ##

    ##
    # UserBadgeLink CRUD
    ##

    #bot.add_cog(GameCog(bot, rest_key))
    return await bot.start(token)
