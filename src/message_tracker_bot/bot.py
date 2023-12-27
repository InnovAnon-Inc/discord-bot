""" The bot proper """

from typing import List, Union, Optional

from discord import ButtonStyle, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ext.commands.errors import CheckFailure
from discord.ui import Button, View
from discord.utils import setup_logging
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked
from re import match as re_match
from re import Match
from discord import Button, ButtonStyle, Interaction, Member, Role, TextChannel

from discord.message import Message
from discord import Embed

from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *
from .crud import *

logger = get_logger()
setup_logging()


@typechecked
class UnfilteredBot(Bot):
    """An overridden version of the Bot class that will listen to other bots."""

    @logerror(logger)
    @trace(logger)
    @typechecked
    async def process_commands(self, message):
        """Override process_commands to listen to bots."""
        ctx:Context = await self.get_context(message)
        await self.invoke(ctx)

pepe_green:int = 0x07c275

@logerror(logger)
@trace(logger)
@typechecked
async def botze(token: str, guild: str, rest_key: str, channel:int, invite_tracker_id:int) -> None:
    """
    scans for messages from InviteTracker
    and interacts with the REST API
    """

    intents: Intents = Intents.default()
    #intents.members = True
    # allow to get commands from GC
    intents.message_content = True  # v2
    bot: Bot = UnfilteredBot(intents=intents, command_prefix='?')

    await bot.add_cog(  BasicCog(bot))
    await bot.add_cog(   TestCog(bot, rest_key, guild, channel))
    #await bot.add_cog(MessageCog(bot, rest_key, invite_tracker_id))

    @bot.event
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_message(message:Message)->None:

        if message.author.id == bot.user.id: # don't process own messages
            await logger.adebug("message author id same as bot user id: %s", message.author.id)
            return

        assert isinstance(message.author.id, int)
        if message.author.id != invite_tracker_id: # only process messages from invitetracker bot
            #assert message.author.id.strip() != invite_tracker_id.strip()
            await logger.ainfo("%s different than %s", message.author.id, invite_tracker_id)
            await bot.process_commands(message)  # Process commands for bot
            return

        my_channel:TextChannel = bot.get_channel(channel)
        assert my_channel is not None
        await logger.ainfo("channel: %s", type(my_channel))

        embed = Embed(title="Message Acknowldged", description="The Invite Tracker Bot sent a message. Parsing it...", color=pepe_green)
        my_message:Message = await my_channel.send(embed=embed)

        # Define the join message format pattern using regular expressions
        #"@<username> has been invited by <user name> and has now <n> invites"
        # https://stackoverflow.com/questions/48354901/how-to-get-the-id-of-a-mentioned-user-in-python-discord-bot
        #message.mentions[0].id
        #message.mentions[0].mention
        #join_message_pattern = r"<@(\d+)> has been invited by (\w+#\d+) and has now (\d+) invites"
        join_message_pattern:str = r"<@(\d+)> has been invited by (\w+)#(\d+) and has now (\d+) invites."

        assert(message.content)

        # Match the message content against the join message pattern
        match:Optional[Match] = re_match(join_message_pattern, message.content)
        if match is None:
            await logger.ainfo("unexpected message format: %s", message.content)
            embed.add_field(name="Unexpected Message Format", value=message.content)

            join_message_pattern = r"<@(\d+)> has been invited by .*"
            match                = re_match(join_message_pattern, message.content)
            msg:str              = "No" if match is None else f"Yes: {match.group(1)}"
            embed.add_field(name="Can match invitee", value=msg)

            join_message_pattern = r".* has been invited by (\w+)#.*"
            match                = re_match(join_message_pattern, message.content)
            msg                  = "No" if match is None else f"Yes: {match.group(1)}"
            embed.add_field(name="Can match inviter", value=msg)

            join_message_pattern = r".*#(\d+) and has now .*"
            match                = re_match(join_message_pattern, message.content)
            msg                  = "No" if match is None else f"Yes: {match.group(1)}"
            embed.add_field(name="Can match channel number", value=msg)

            join_message_pattern = r".* and has now (\d+) invites."
            match                = re_match(join_message_pattern, message.content)
            msg                  = "No" if match is None else f"Yes: {match.group(1)}"
            embed.add_field(name="Can match invite count", value=msg)

            await my_message.edit(embed=embed)

            return

        member_id      :int = int(match.group(1))
        inviter        :str =     match.group(2)
        your_channel   :int = int(match.group(3))
        inviter_invites:int = int(match.group(4))

        # Print the extracted information
        #await logger.ainfo("Member Mention: %s", member_mention)
        await logger.ainfo("Inviter: %s", inviter)
        await logger.ainfo("Inviter Invites: %s", inviter_invites)
        #await logger.ainfo("Mentioned User ID: %s", mentioned_user_id)

        embed.add_field(name="Member ID", value=f"{member_id}")
        embed.add_field(name="Inviter",   value=f"{inviter}")
        embed.add_field(name="Channel",   value=f"{your_channel}")
        embed.add_field(name="Invites",   value=f"{inviter_invites}")
        await my_message.edit(embed=embed)

        my_user: JSON = await api_get_user(rest_key, inviter)
        if not my_user:
            created_user: str = await api_create_user(rest_key, inviter)
            await logger.ainfo("created user: %s", created_user)

            embed.add_field(name="Register User Result",    value=f"{created_user} (success)")
            await my_message.edit(embed=embed)

        result:str = await api_set_user_invite_count(rest_key, inviter, inviter_invites)
        embed.add_field(name="Set Invite Count Result", value=f"{result} (success)")
        await my_message.edit(embed=embed)

    return await bot.start(token)

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, Botze, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
