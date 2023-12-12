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

from .rest import api_get
from .rest import api_post
from .rest import api_delete
from .types import JSON
from .types import HEADERS
from .types import DATA
from .types import PARAMS

logger = get_logger()

##
# User CRUD
##

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_users(rest_key:str) -> JSON:
    url:str = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user?select=*'
    params:PARAMS = {
        'select': '*',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    return await api_get(url, params, headers)

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_user(rest_key:str, name:str) -> JSON:
    url:str = f'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user'
    params:PARAMS = {
        'name': f'eq.{name}',
        'select': '*',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',

    }
    return await api_get(url, params, headers)

@logerror(logger)
@trace(logger)
@typechecked
async def api_create_user(rest_key:str, name:str) -> str:
    url:str = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user'
    params:PARAMS = {}
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    data:DATA = {
        'name': name,
        #'unclaimed_codes' : 10,
        #`number_invites': 0,
    }
    return await api_post(url, params, headers, data)

@logerror(logger)
@trace(logger)
@typechecked
async def api_delete_user(rest_key:str, name:str) -> str:
    url:str = f'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1/user'
    params:PARAMS = {
        'name': f'eq.{name}',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    return await api_delete(url, params, headers)
