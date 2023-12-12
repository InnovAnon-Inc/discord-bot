from os import getenv
from typing import List
from random import choice
from typing import Dict
from typing import Any
from typing import Union
from aiohttp import ClientSession
from urllib.parse import urlencode

from discord import Intents
from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import has_role
from discord.utils import setup_logging
from discord.utils import get
from discord.utils import find
from discord.ui import Button
from discord import ButtonStyle
from discord import Interaction
from discord import Member
from discord.ui import View
from structlog import get_logger
from typeguard import typechecked
from discord.ext.commands.errors import CheckFailure

from .hello import hellomain
from .types import P
from .log import trace
from .log import logerror
from .log import logres

logger = get_logger()
setup_logging()



@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def is_admin(ctx)->bool:
    # TODO type hints
    admin_role = get(ctx.guild.roles, name='admin')
    return admin_role in ctx.author.roles

@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def get_arg(ctx)->str:
    return ctx.message.content.split(maxsplit=1)[1] # Extract the arg from the command message
