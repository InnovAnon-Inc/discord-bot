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

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, name
@typechecked
async def api_get2(rest_key:str, table:str, user_id:int, game_id:int, params:PARAMS=ALL_FIELDS) -> JSON:
    url:str = '/'.join([REST_API, table])
    params = dict(params)

    assert not ('user_id' in params), f'params should not contain a `user_id` key, but params is {params}'
    params['user_id'] = f'eq.{user_id}'

    assert not ('game_id' in params), f'params should not contain a `game_id` key, but params is {params}'
    params['game_id'] = f'eq.{game_id}'

    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    result:JSON = await rest_get(url, params, headers)
    return result

@logerror(logger)
@trace(logger)
@logargswl(logger,1,2) # table, name
@typechecked
async def api_delete2(rest_key:str, table:str, user_id:int, game_id:int) -> str:
    url:str = '/'.join([REST_API, table])
    params:PARAMS = {
        'user_id': f'eq.{user_id}',
        'game_id': f'eq.{game_id}',
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
async def api_update2(rest_key:str, table:str, user_id:int, game_id:int, data:DATA) -> str:
    url:str = '/'.join([REST_API, table])
    params:PARAMS = {
        'user_id': f'eq.{user_id}',
        'game_id': f'eq.{game_id}',
    }
    headers:HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_patch(url, params, headers, data)


##
# User CRUD
##

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_codes(rest_key:str) -> JSON:
    params:PARAMS = {
        #'select': 'name',
        'select': '*',
    }
    return await api_gets(rest_key, 'code', params)

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_code(rest_key:str, user_name:str, game_name:str) -> JSON:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    result:JSON = await api_get2(rest_key, 'code', user_id, game_id)
    assert len(result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]

#@logerror(logger)
@trace(logger)
@typechecked
async def api_create_code(rest_key:str, user_name:str, game_name:str) -> str:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    data:DATA = {
        'user_id': str(user_id),
        'game_id': str(game_id),
        # remaining_uses: 10
        # secret: random()
    }
    return await api_create(rest_key, 'code', data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_delete_code(rest_key:str, user_name:str, game_name:str) -> str:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    return await api_delete2(rest_key, 'code', user_id, game_id)

##@logerror(logger)
#@trace(logger)
#@typechecked
#async def api_rename_code(rest_key:str, name:str, new_name:str) -> str:
#    data:DATA = {
#        'name': new_name,
#    }
#    return await api_update2(rest_key, 'code', name, data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_code_remaining_uses(rest_key:str, user_name:str, game_name:str) -> JSON:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    params:PARAMS = {
        'select': 'remaining_uses',
    }
    result:JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]

@typechecked
async def api_get_code_secret(rest_key:str, user_name:str, game_name:str) -> JSON:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    params:PARAMS = {
        'select': 'secret',
    }
    result:JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]

#@logerror(logger)
@trace(logger)
@typechecked
async def api_set_code_remaining_uses(rest_key:str, user_name:str, game_name:str, remaining_uses:int) -> str:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    data:DATA = {
        'remaining_uses': str(remaining_uses),
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_set_code_secret(rest_key:str, user_name:str, game_name:str, secret:int) -> str:
    user_id:int = await api_get_user_id(rest_key, user_name)
    game_id:int = await api_get_game_id(rest_key, game_name)
    data:DATA = {
        'secret': str(secret),
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)
