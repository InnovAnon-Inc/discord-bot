from typing import Tuple
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
from .log import logargswl

logger = get_logger()

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
#@logargswl(logger, 1)
#@logres(logger)
@typechecked
async def arg_helper(ctx, n:int)->List[str]:
    args:List[str] = ctx.message.content.split()
    cmd :str       = args[0]
    args           = args[1:]
    if len(args) != n:
        raise ValueError(f'Command {cmd} expects {n} argument(s), but you gave {len(args)}: {args}')
    return args


@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def get_arg(ctx)->str:
    #return ctx.message.content.split(maxsplit=1)[1] # Extract the arg from the command message
    args:List[str] = await arg_helper(ctx, 1)
    return args[0]

@logerror(logger)
@trace(logger)
@logargswl(logger, 1)
@logres(logger)
@typechecked
async def get_args(ctx, n:int)->List[str]:
    #args:List[str] = ctx.message.content.split(maxsplit=n)[1:] # Extract n args from the command message
    return await arg_helper(ctx, n)
