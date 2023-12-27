#! /usr/bin/env python

""" The bot proper """

from asyncio import run
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


logger = get_logger()


async def fuck():
        message:str = """<@1189695016180924436> has been invited by programmer_palpatine_06045#0 and has now 0 invites."""
        join_message_pattern:str = r"<@(\d+)> has been invited by (\w+)#(\d+) and has now (\d+) invites."
        match:Optional[Match] = re_match(join_message_pattern, message)
        if match is None:
            await logger.ainfo("unexpected message format: %s", message)

            join_message_pattern = r"<@(\d+)> has been invited by .*"
            match                = re_match(join_message_pattern, message)
            msg:str              = "No" if match is None else "Yes"
            await logger.ainfo("Can match invitee: %s", msg)

            join_message_pattern = r".* has been invited by (\w+)#.*"
            match                = re_match(join_message_pattern, message)
            msg                  = "No" if match is None else "Yes"
            await logger.ainfo("Can match inviter: %s", msg)

            join_message_pattern = r".*#(\d+) and has now .*"
            match                = re_match(join_message_pattern, message)
            msg                  = "No" if match is None else "Yes"
            await logger.ainfo("Can match channel number: %s", msg)

            join_message_pattern = r".* and has now (\d+) invites."
            match                = re_match(join_message_pattern, message)
            msg                  = "No" if match is None else "Yes"
            await logger.ainfo("Can match invite count: %s", msg)

            await message.edit(embed=embed)

            return
        print('what the fuck')
run(fuck())
