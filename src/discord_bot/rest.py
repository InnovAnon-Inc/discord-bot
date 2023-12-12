from os import getenv
from typing import List
from random import choice
from typing import Dict
from typing import Any
from typing import Union
from typing import Callable
from typing import TypeVar
from urllib.parse import urlencode
from functools import wraps

from aiohttp import ClientSession
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
from .types import JSON
from .types import HEADERS
from .types import DATA
from .types import PARAMS
from .log import logres
from .log import logargswl

logger = get_logger()
setup_logging()

class RestException(Exception):
    """ """

##
# CRUD Helpers
##

@logerror(logger)
@trace(logger)
@typechecked
async def api_encode(base_url:str, params:PARAMS) -> str:
    encoded_params:str = urlencode(params)
    return f'{base_url}?{encoded_params}'

RestT        = TypeVar('RestT', JSON, str)
CallableApi  = Callable[[str,PARAMS,P.args,P.kwargs],RestT]
CallableRest = Callable[[str,       P.args,P.kwargs],RestT]
#WrapperRest  = Callable[[CallableRest], CallableApi]

#@logerror(logger)
@typechecked
#@logres(logger) # not async
def rest_api(func:CallableRest)->CallableApi:
    @wraps(func)
    async def wrapper(base_url:str, params:PARAMS, *args:P.args, **kwargs:P.kwargs)->RestT:
        url:str = await api_encode(base_url, params)
        return await func(url, *args, **kwargs)
    return wrapper

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@typechecked
@rest_api
@typechecked
#async def api_get(base_url:str, params:PARAMS, headers:HEADERS) -> JSON:
async def api_get(url:str, headers:HEADERS, *args:P.args, **kwargs:P.kwargs) -> JSON:
    assert not args
    assert not kwargs
    #await logger.adebug('api_get()')
    #await logger.adebug('url: %s', url)
    #url:str = await api_encode(base_url, params)
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                #await logger.adebug('data: %s', data)
                return data
            else:
                raise RestException(f"Failed to get games. HTTP status code: {response.status}")

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@typechecked
@rest_api
@typechecked
#async def api_post(base_url:str, params:PARAMS, headers:HEADERS, data:DATA) -> str:
async def api_post(url:str, headers:HEADERS, data:DATA, *args:P.args, **kwargs:P.kwargs) -> str:
    assert not args
    assert not kwargs
    #await logger.adebug('api_post()')
    #await logger.adebug('url: %s', url)
    #url:str = await api_encode(base_url, params)
    async with ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 201:
                created_game = await response.text()
                #await logger.adebug('created: %s', created_game)
                return created_game
            else:
                raise RestException(f"Failed to create game. HTTP status code: {response.status}")

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@typechecked
@rest_api
@typechecked
#async def api_delete(base_url:str, params:PARAMS,headers:HEADERS) -> str:
async def api_delete(url:str, headers:HEADERS, *args:P.args, **kwargs:P.kwargs) -> str:
    assert not args
    assert not kwargs
    #url:str = await api_encode(base_url, params)
    #await logger.adebug('api_delete()')
    #await logger.adebug('url: %s', url)
    async with ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                deleted_game = await response.text()
                #await logger.adebug('deleted: %s', deleted_game)
                return deleted_game
            else:
                raise RestException(f"Failed to delete game. HTTP status code: {response.status}")
