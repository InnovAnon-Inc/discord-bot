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

class RestException(Exception):
    """ """

##
# REST API CRUD Helpers
##

@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def rest_encode(base_url:str, params:PARAMS) -> str:
    encoded_params:str = urlencode(params)
    return f'{base_url}?{encoded_params}'

RestT        = TypeVar('RestT', JSON, str)
CallableApi  = Callable[[str,PARAMS,       HEADERS,P.args,P.kwargs],RestT]
CallableRest = Callable[[str,ClientSession,HEADERS,P.args,P.kwargs],RestT]
#WrapperRest  = Callable[[CallableRest], CallableApi]

#@logerror(logger) # not async
@typechecked
#@logres(logger) # not async
def rest_params(func:CallableRest)->CallableApi:
    @wraps(func)
    async def wrapper(base_url:str, params:PARAMS, *args:P.args, **kwargs:P.kwargs)->RestT:
        url:str = await rest_encode(base_url, params)
        async with ClientSession() as session:
            return await func(url, session, *args, **kwargs)
    return wrapper

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@logres(logger)
@typechecked
@rest_params # rewrites siggy
@logargswl(logger,0) # url
@typechecked
async def rest_get(url:str, session:ClientSession, headers:HEADERS, *args:P.args, **kwargs:P.kwargs) -> JSON:
    assert not args
    assert not kwargs
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise RestException(f"Failed to get. HTTP status code: {response.status}")
        return await response.json()

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@logres(logger)
@typechecked
@rest_params # rewrites siggy
@logargswl(logger,0) # url
@typechecked
async def rest_post(url:str, session:ClientSession, headers:HEADERS, data:DATA, *args:P.args, **kwargs:P.kwargs) -> str:
    assert not args
    assert not kwargs
    async with session.post(url, headers=headers, json=data) as response:
        if response.status != 201:
            raise RestException(f"Failed to post. HTTP status code: {response.status}")
        return await response.text()

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@logres(logger)
@typechecked
@rest_params # rewrites siggy
@logargswl(logger,0) # url
@typechecked
async def rest_delete(url:str, session:ClientSession, headers:HEADERS, *args:P.args, **kwargs:P.kwargs) -> str:
    assert not args
    assert not kwargs
    async with session.delete(url, headers=headers) as response:
        if response.status != 204:
            raise RestException(f"Failed to delete. HTTP status code: {response.status}")
        return await response.text()

@logerror(logger)
@trace(logger)
@logargswl(logger,0,1) # base_url, params
@logres(logger)
@typechecked
@rest_params # rewrites siggy
@logargswl(logger,0) # url
@typechecked
async def rest_patch(url:str, session:ClientSession, headers:HEADERS, data:DATA, *args:P.args, **kwargs:P.kwargs) -> str:
    assert not args
    assert not kwargs
    async with session.patch(url, headers=headers, json=data) as response:
        if response.status != 204:
            raise RestException(f"Failed to patch. HTTP status code: {response.status}")
        return await response.text()
