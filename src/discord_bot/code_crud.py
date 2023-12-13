""" Game Table CRUD """

from typing import List
from typing import Dict

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_gets, ALL_FIELDS, REST_API
from .log import logerror, trace, logargswl
from .types import DATA, HEADERS, JSON, PARAMS
from .user_crud import api_get_user_id
from .game_crud import api_get_game_id
from .user_crud import api_get_user_by_id
from .game_crud import api_get_game_by_id
from .rest import rest_get, rest_delete, rest_patch
from .util import get_user_ids, get_game_ids, get_remainings, get_secrets, get_names

logger = get_logger()

##
# TODO the api funcs should be deduplicated
##


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, name
@typechecked
async def api_get2(
        rest_key: str, table: str,
        user_id: int, game_id: int,
        params: PARAMS = ALL_FIELDS) -> JSON:
    """ get the row with the specified `name` """

    url: str = '/'.join([REST_API, table])
    params = dict(params)

    assert 'user_id' not in params, f'params should not contain a `user_id` key, but params is {params}'
    params['user_id'] = f'eq.{user_id}'

    assert 'game_id' not in params, f'params should not contain a `game_id` key, but params is {params}'
    params['game_id'] = f'eq.{game_id}'

    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    result: JSON = await rest_get(url, params, headers)
    return result


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, name
@typechecked
async def api_delete2(
        rest_key: str, table: str,
        user_id: int, game_id: int) -> str:
    """ do a delete operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'user_id': f'eq.{user_id}',
        'game_id': f'eq.{game_id}',
    }
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    return await rest_delete(url, params, headers)


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, data
@typechecked
async def api_update2(
        rest_key: str, table: str,
        user_id: int, game_id: int, data: DATA) -> str:
    """ do an update/patch operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'user_id': f'eq.{user_id}',
        'game_id': f'eq.{game_id}',
    }
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_patch(url, params, headers, data)


##
# User CRUD
##

# @logerror(logger)
@trace(logger)
@typechecked
async def api_get_codes(rest_key: str) -> JSON:
    """ Get the all fields except `secret` of all registered codes """

    params: PARAMS = {
        # 'select': 'name',
        'select': 'user_id,game_id,remaining',
    }
    result:JSON = await api_gets(rest_key, 'code', params)

    user_ids  :List[int] = get_user_ids(result)
    game_ids  :List[int] = get_game_ids(result)
    remainings:List[int] = get_remainings(result)

    #user_names:List[str] = list(map(api_get_user_by_id, user_ids))
    #game_names:List[str] = list(map(api_get_game_by_id, game_ids))
    user_dicts:List[Dict[str,str]] = [await api_get_user_by_id(rest_key, user_id) for user_id in user_ids]
    game_dicts:List[Dict[str,str]] = [await api_get_game_by_id(rest_key, game_id) for game_id in game_ids]

    user_names:List[str] = get_names(user_dicts)
    game_names:List[str] = get_names(game_dicts)

    rows:List[Dict[str,str]] = [ {
        'user_name': user_name,
        'game_name': game_name,
        'remaining': str(remaining),
    } for user_name, game_name, remaining in zip(user_names, game_names, remainings)]
    return rows




@logerror(logger)
@trace(logger)
@typechecked
async def api_get_code(rest_key: str, user_name: str, game_name: str) -> JSON:
    """ Get all columns of the code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    result: JSON = await api_get2(rest_key, 'code', user_id, game_id)
    assert len(
        result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]

# @logerror(logger)


@trace(logger)
@typechecked
async def api_create_code(rest_key: str, user_name: str, game_name: str, secret:str) -> str:
    """ Register a code """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'user_id': str(user_id),
        'game_id': str(game_id),
        # remaining: 10
        # TODO
        # secret: random()
        'secret': secret,
    }
    return await api_create(rest_key, 'code', data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_delete_code(rest_key: str, user_name: str, game_name: str) -> str:
    """ Unregister a code """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    return await api_delete2(rest_key, 'code', user_id, game_id)

# @logerror(logger)
# @trace(logger)
# @typechecked
# async def api_rename_code(rest_key:str, name:str, new_name:str) -> str:
#    data:DATA = {
#        'name': new_name,
#    }
#    return await api_update2(rest_key, 'code', name, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_code_remaining(rest_key: str, user_name: str, game_name: str) -> int:
    """ Get the `remaining` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    params: PARAMS = {
        'select': 'remaining',
    }
    result: JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(
        result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['remaining'])


@typechecked
async def api_get_code_secret(rest_key: str, user_name: str, game_name: str) -> str:
    """ Get the `secret` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    params: PARAMS = {
        'select': 'secret',
    }
    result: JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(
        result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]['secret']

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_code_remaining(
        rest_key: str, user_name: str, game_name: str,
        remaining: int) -> str:
    """ Set the `remaining` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'remaining': str(remaining),
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_code_secret(rest_key: str, user_name: str, game_name: str,
                              secret: str) -> str:
    """ Set the `secret` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'secret': secret,
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)
