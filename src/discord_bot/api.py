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

from .rest import rest_get
from .rest import rest_post
from .rest import rest_delete
from .rest import rest_patch
from .types import JSON
from .types import HEADERS
from .types import DATA
from .types import PARAMS

logger = get_logger()

REST_API:str = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1'
ALL_FIELDS:PARAMS = {
    'select': '*',
}

##
# Supabase REST API CRUD Helpers
##

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, name
@typechecked
async def api_gets(rest_key:str, table:str, params:PARAMS=ALL_FIELDS) -> JSON:
    url:str = '/'.join([REST_API, table])
    #params:PARAMS = {
    #    'select': '*',
    #}
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    return await rest_get(url, params, headers)

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, name
@typechecked
async def api_get(rest_key:str, table:str, name:str, params:PARAMS=ALL_FIELDS) -> JSON:
    await logger.adebug('api_get() 1')
    url:str = '/'.join([REST_API, table])
    await logger.adebug('api_get() 2')
    #params:PARAMS = {
    #    'name': f'eq.{name}',
    #    'select': '*',
    #}
    await logger.adebug('api_get() 3')
    assert not ('name' in params), f'params should not contain a `name` key, but params is {params}'
    await logger.adebug('api_get() 4')
    params = dict(params)
    await logger.adebug('api_get() 5')
    params['name'] = f'eq.{name}'
    await logger.adebug('api_get() 6')
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    await logger.adebug('api_get() 7')
    result:JSON = await rest_get(url, params, headers)
    await logger.adebug('api_get() 8')
    return result

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, data
@typechecked
async def api_create(rest_key:str, table:str, data:DATA) -> str:
    url:str = '/'.join([REST_API, table])
    params:PARAMS = {}
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_post(url, params, headers, data)

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, name
@typechecked
async def api_delete(rest_key:str, table:str, name:str) -> str:
    url:str = '/'.join([REST_API, table])
    params:PARAMS = {
        'name': f'eq.{name}',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    return await rest_delete(url, params, headers)

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, data
@typechecked
async def api_update(rest_key:str, table:str, name:str, data:DATA) -> str:
    url:str = '/'.join([REST_API, table])
    params:PARAMS = {
        'name': f'eq.{name}',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_patch(url, params, headers, data)
