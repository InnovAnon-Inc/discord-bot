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

from .types import JSON
from .types import HEADERS
from .types import DATA
from .types import PARAMS

from .api import api_get
from .api import api_gets
from .api import api_create
from .api import api_delete
from .api import api_update

logger = get_logger()

##
# User CRUD
##

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_users(rest_key:str) -> JSON:
    return await api_gets(rest_key, 'user')

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_user(rest_key:str, name:str) -> JSON:
    return await api_get(rest_key, 'user', name)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_create_user(rest_key:str, name:str) -> str:
    data:DATA = {
        'name': name,
        #'unclaimed_codes' : 10,
        #`number_invites': 0,
    }
    return await api_create(rest_key, 'user', data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_delete_user(rest_key:str, name:str) -> str:
    return await api_delete(rest_key, 'user', name)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_rename_user(rest_key:str, name:str, new_name:str) -> str:
    data:DATA = {
        'name': new_name,
    }
    return await api_update(rest_key, 'user', name, data)
# TODO get/set invite count
# TODO get/set unclaimed codes
