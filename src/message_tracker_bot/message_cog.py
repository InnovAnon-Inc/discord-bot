""" Message tracking functionality """

from typing import List, Union

from discord import ButtonStyle, Intents  # , Interaction, Member, Message
from discord.ext.commands import Bot, has_role, Context
from discord.ext.commands.errors import CheckFailure
from discord.ui import Button, View
from discord.utils import setup_logging
from discord.ext.commands import Cog
from structlog import get_logger
from typeguard import typechecked

from .log import logerror, trace
from .types import JSON
from .util import get_arg, get_args, is_admin
from .cogs import *
from .user_crud import api_get_user_invite_count, api_set_user_invite_count

logger = get_logger()
setup_logging()


# TODO invite tracker
#invites = {}
#last = ""

@typechecked
class MessageCog(Cog):
    """ Message-related functionality """

    @typechecked
    def __init__(self, bot:Bot, rest_key:str, invite_tracker_id:str):
        self.bot               = bot
        self.rest_key          = rest_key
        self.invite_tracker_id = invite_tracker_id

    @Cog.listener()
    @logerror(logger)
    @trace(logger)
    @typechecked
    async def on_message(self, message):

        # don't process own messages
        if message.author.id == self.bot.user.id:
            return

        # only process messages from invitetracker bot
        if message.author.id != invite_tracker_id:
            return


        # TODO get expected user id for invitetracker bot

        #"@<username> has been invited by <user name> and has now <n> invites"
        # https://stackoverflow.com/questions/48354901/how-to-get-the-id-of-a-mentioned-user-in-python-discord-bot
        #message.mentions[0].id
        #message.mentions[0].mention
        # Invite Tracker#0478

        # Define the join message format
        join_message_format = "{member_mention} has been invited by {inviter} and has now {inviter_invites} invites"

        # Check if the message matches the join message format
        if message.content == join_message_format:
            # Extract the required information from the message
            member_mention = message.mentions[0].mention
            inviter = message.content.split(" ")[-4]  # Get the second last word
            inviter_invites = int(message.content.split(" ")[-2])  # Get the last word
    
            # TODO: Use the extracted information as needed
            # For example, you can access the user ID of the mentioned user using `message.mentions[0].id`
            mentioned_user_id = message.mentions[0].id

            # Print the extracted information
            print(f"Member Mention: {member_mention}")
            print(f"Inviter: {inviter}")
            print(f"Inviter Invites: {inviter_invites}")
            print(f"Mentioned User ID: {mentioned_user_id}")

            invite_count:int = await api_get_user_unclaimed_codes(self.rest_key, member_user_id)
            await api_set_user_unclaimed_codes(self.rest_key, member_user_id, invite_count + 1)
            

        # Handle other cases or do additional processing here
        # ...


