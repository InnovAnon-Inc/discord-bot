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
from .util import get_names

logger = get_logger()

##
# Game CRUD
##

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_games(rest_key:str) -> List[str]:
    params:PARAMS = {
        'select': 'name',
    }
    result:JSON = await api_gets(rest_key, 'game', params)
    return get_names(result)

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_game(rest_key:str, name:str) -> JSON:
    await logger.adebug('api_get_game() 1')
    result:JSON = await api_get(rest_key, 'game', name)
    await logger.adebug('api_get_game() 2')
    assert len(result) == 1, f'api_get_game() result len should be 1, but it is {len(result)} {result}'
    await logger.adebug('api_get_game() 3')
    return result[0]

#@logerror(logger)
@trace(logger)
@typechecked
async def api_create_game(rest_key:str, name:str) -> str:
    data:DATA = {
        'name': name,
    }
    return await api_create(rest_key, 'game', data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_delete_game(rest_key:str, name:str) -> str:
    return await api_delete(rest_key, 'game', name)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_rename_game(rest_key:str, name:str, new_name:str) -> str:
    data:DATA = {
        'name': new_name,
    }
    return await api_update(rest_key, 'game', name, data)

#@logerror(logger)
@trace(logger)
@typechecked
async def api_get_game_id(rest_key:str, name:str) -> int:
    params:PARAMS = {
        'select': 'id',
    }
    result:JSON = await api_get(rest_key, 'game', name, params)
    assert len(result) == 1, f'api_get_game() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['id'])
