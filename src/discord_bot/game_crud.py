""" Game Table CRUD """

from typing import List

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_delete, api_get, api_gets, api_update, api_get_by_id
from .log import logerror, trace
from .types import DATA, JSON, PARAMS
from .util import get_names

logger = get_logger()

##
# Game CRUD
##

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_games(rest_key: str) -> List[str]:
    """ Get the `name` of all registered games """

    params: PARAMS = {
        'select': 'name',
    }
    result: JSON = await api_gets(rest_key, 'game', params)
    return get_names(result)


@logerror(logger)
@trace(logger)
@typechecked
async def api_get_game(rest_key: str, name: str) -> JSON:
    """ Get all columns of the game with `name` """

    result: JSON = await api_get(rest_key, 'game', name)
    assert len(
        result) == 1, f'api_get_game() result len should be 1, but it is {len(result)} {result}'
    return result[0]

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_game_by_id(rest_key: str, game_id:int) -> JSON:
    """ Get all columns of the game with `name` """

    params: PARAMS = {
        'select': 'name',
    }
    result: JSON = await api_get_by_id(rest_key, 'game', str(game_id), params)
    assert len(
        result) == 1, f'api_get_game() result len should be 1, but it is {len(result)} {result}'
    return result[0]

# @logerror(logger)


@trace(logger)
@typechecked
async def api_create_game(rest_key: str, name: str) -> str:
    """ Register a game """

    data: DATA = {
        'name': name,
    }
    return await api_create(rest_key, 'game', data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_delete_game(rest_key: str, name: str) -> str:
    """ Unregister a game """

    return await api_delete(rest_key, 'game', name)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_rename_game(rest_key: str, name: str, new_name: str) -> str:
    """ Change a game's name """

    data: DATA = {
        'name': new_name,
    }
    return await api_update(rest_key, 'game', name, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_game_id(rest_key: str, game_id: str) -> int:
    """ Get the `id` of the game with `game_id` """

    params: PARAMS = {
        'select': 'id',
    }
    result: JSON = await api_get(rest_key, 'game', str(game_id), params)
    assert len(
        result) == 1, f'api_get_game() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['id'])
