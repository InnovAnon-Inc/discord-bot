""" The bot proper """

from typing import List, Union

from discord import ButtonStyle, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ext.commands.errors import CheckFailure
from discord.ui import Button, View
from discord.utils import setup_logging
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked
import re

from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *
from .crud import *

logger = get_logger()
setup_logging()


# TODO invite tracker
#invites = {}
#last = ""

##
# 0xPepesPlay Bot
##

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


@logerror(logger)
@trace(logger)
@typechecked
async def botze(token: str, guild: str, rest_key: str, channel:str, invite_tracker_id:int) -> None:
    """
    scans for messages from InviteTracker
    and interacts with the REST API
    """

    intents: Intents = Intents.default()
    #intents.members = True
    # allow to get commands from GC
    intents.message_content = True  # v2
    # ChatGPT:
    # Change the type of bot from discord.ext.commands.Bot to discord.ext.commands.Bot.
    # This ensures that the event loop is properly managed by the commands.Bot class.
    bot: Bot = UnfilteredBot(intents=intents, command_prefix='?')
    # games_list:JSON = []


    await bot.add_cog(  BasicCog(bot))
    await bot.add_cog(   TestCog(bot, rest_key, guild, channel))
    #await bot.add_cog(MessageCog(bot, rest_key, invite_tracker_id))

    @bot.event
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_message(message):

        # don't process own messages
        if message.author.id == bot.user.id:
            await logger.adebug("message author id same as bot user id: %s", message.author.id)
            return

        # only process messages from invitetracker bot
        assert isinstance(message.author.id, int)
        if message.author.id != invite_tracker_id:
            #assert message.author.id.strip() != invite_tracker_id.strip()
            await logger.ainfo("%s different than %s", message.author.id, invite_tracker_id)
            await bot.process_commands(message)  # Process commands for bot
            return


        # Define the join message format pattern using regular expressions
        #"@<username> has been invited by <user name> and has now <n> invites"
        # https://stackoverflow.com/questions/48354901/how-to-get-the-id-of-a-mentioned-user-in-python-discord-bot
        #message.mentions[0].id
        #message.mentions[0].mention
        #join_message_pattern = r"<@(\d+)> has been invited by (\w+#\d+) and has now (\d+) invites"
        join_message_pattern = r"<@(\d+)> has been invited by (\w+)#\d+ and has now (\d+) invites"

        # Match the message content against the join message pattern
        match = re.match(join_message_pattern, message.content)
        if match:
            member_id = match.group(1)  # Extract the member ID
            inviter = match.group(2)  # Extract the inviter
            inviter_invites = match.group(3)  # Extract the number of invites

            # Format the expected join message using the extracted information
            #expected_join_message = join_message_format.format(member_id=member_id, inviter=inviter, inviter_invites=inviter_invites)

            # Compare the actual and expected join messages
            #if message.content == expected_join_message:
                # The message matches the expected format
                # Handle the join message here
            #    pass


            #member_mention = message.mentions[0].mention
            #inviter = message.content.split(" ")[-4]  # Get the second last word
            #inviter_invites = int(message.content.split(" ")[-2])  # Get the last word
    
            # TODO: Use the extracted information as needed
            # For example, you can access the user ID of the mentioned user using `message.mentions[0].id`
            #mentioned_user_id = message.mentions[0].id

            # Print the extracted information
            #await logger.ainfo("Member Mention: %s", member_mention)
            await logger.ainfo("Inviter: %s", inviter)
            await logger.ainfo("Inviter Invites: %s", inviter_invites)
            #await logger.ainfo("Mentioned User ID: %s", mentioned_user_id)

            invite_count:int = await api_get_user_unclaimed_codes(rest_key, inviter)
            await api_set_user_unclaimed_codes(rest_key, inviter, invite_count + 1)
            return

        await logger.ainfo("unexpected message format: %s", message.content)

        # ChatGPT says this will somehow cause the on_message() event to be triggered
            

        # Handle other cases or do additional processing here
        # ...


    return await bot.start(token)
