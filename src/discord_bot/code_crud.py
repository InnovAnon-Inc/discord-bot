""" Game Table CRUD """

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_gets, ALL_FIELDS, REST_API
from .log import logerror, trace, logargswl
from .types import DATA, HEADERS, JSON, PARAMS
from .user_crud import api_get_user_id
from .game_crud import api_get_game_id
from .rest import rest_get, rest_delete, rest_patch

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

    assert 'user_id' not in params,
    f'params should not contain a `user_id` key, but params is {params}'
    params['user_id'] = f'eq.{user_id}'

    assert 'game_id' not in params,
    f'params should not contain a `game_id` key, but params is {params}'
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
        # TODO not secret
        'select': '*',
    }
    return await api_gets(rest_key, 'code', params)


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
async def api_create_code(rest_key: str, user_name: str, game_name: str) -> str:
    """ Register a code """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'user_id': str(user_id),
        'game_id': str(game_id),
        # remaining_uses: 10
        # secret: random()
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
async def api_get_code_remaining_uses(rest_key: str, user_name: str, game_name: str) -> JSON:
    """ Get the `remaining_uses` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    params: PARAMS = {
        'select': 'remaining_uses',
    }
    result: JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(
        result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]


@typechecked
async def api_get_code_secret(rest_key: str, user_name: str, game_name: str) -> JSON:
    """ Get the `secret` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    params: PARAMS = {
        'select': 'secret',
    }
    result: JSON = await api_get2(rest_key, 'code', user_id, game_id, params)
    assert len(
        result) == 1, f'api_get_code() result len should be 1, but it is {len(result)} {result}'
    return result[0]

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_code_remaining_uses(
        rest_key: str, user_name: str, game_name: str,
        remaining_uses: int) -> str:
    """ Set the `remaining_uses` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'remaining_uses': str(remaining_uses),
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_code_secret(rest_key: str, user_name: str, game_name: str,
                              secret: int) -> str:
    """ Set the `secret` of the access code with `user_name` and `game_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    game_id: int = await api_get_game_id(rest_key, game_name)
    data: DATA = {
        'secret': str(secret),
    }
    return await api_update2(rest_key, 'code', user_id, game_id, data)
