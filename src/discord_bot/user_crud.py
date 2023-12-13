""" User Table CRUD """

from typing import List

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_delete, api_get, api_gets, api_update
from .log import logerror, trace
from .types import DATA, JSON, PARAMS
from .util import get_names

logger = get_logger()

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_users(rest_key: str) -> List[str]:
    """ Get the `name` of all registered users """

    params: PARAMS = {
        'select': 'name',
    }
    result: JSON = await api_gets(rest_key, 'user', params)
    return get_names(result)


@logerror(logger)
@trace(logger)
@typechecked
async def api_get_user(rest_key: str, name: str) -> JSON:
    """ Get all columns of the user with `name` """

    result: JSON = await api_get(rest_key, 'user', name)
    assert len(
        result) == 1, f'api_get_user() result len should be 1, but it is {len(result)} {result}'
    return result[0]

# @logerror(logger)


@trace(logger)
@typechecked
async def api_create_user(rest_key: str, name: str) -> str:
    """ Register a user """

    data: DATA = {
        'name': name,
        # 'unclaimed_codes' : 10,
        # `number_invites': 0,
    }
    return await api_create(rest_key, 'user', data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_delete_user(rest_key: str, name: str) -> str:
    """ Unregister a user """

    return await api_delete(rest_key, 'user', name)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_rename_user(rest_key: str, name: str, new_name: str) -> str:
    """ Change a user's name """

    data: DATA = {
        'name': new_name,
    }
    return await api_update(rest_key, 'user', name, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_user_id(rest_key: str, name: str) -> int:
    """ Get the `id` of the user with `name` """

    params: PARAMS = {
        'select': 'id',
    }
    result: JSON = await api_get(rest_key, 'user', name, params)
    assert len(
        result) == 1, f'api_get_user() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['id'])

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_user_invite_count(rest_key: str, name: str) -> int:
    """ Get the `invite_count` of the user with `name` """

    params: PARAMS = {
        'select': 'invite_count',
    }
    result: JSON = await api_get(rest_key, 'user', name, params)
    assert len(
        result) == 1, f'api_get_user() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['invite_count'])

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_user_unclaimed_codes(rest_key: str, name: str) -> int:
    """ Get the `unclaimed_codes` of the user with `name` """

    params: PARAMS = {
        'select': 'unclaimed_codes',
    }
    result: JSON = await api_get(rest_key, 'user', name, params)
    assert len(
        result) == 1, f'api_get_user() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['unclaimed_codes'])

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_user_invite_count(rest_key: str, name: str, invite_count: int) -> str:
    """ Set the `invite_count` of the user with `name` """

    data: DATA = {
        'invite_count': str(invite_count),
    }
    return await api_update(rest_key, 'user', name, data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_set_user_unclaimed_codes(rest_key: str, name: str, unclaimed_codes: int) -> str:
    """ Set the `unclaimed_codes` of the user with `name` """

    data: DATA = {
        'unclaimed_codes': str(unclaimed_codes),
    }
    return await api_update(rest_key, 'user', name, data)
