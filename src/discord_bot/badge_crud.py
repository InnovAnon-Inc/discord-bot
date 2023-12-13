""" Badge Table CRUD """

from typing import List

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_delete, api_get, api_gets, api_update, api_get_by_id
from .log import trace, logerror
from .types import DATA, JSON, PARAMS
from .util import get_names

logger = get_logger()

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_badges(rest_key: str) -> List[str]:
    """ Get the `name` of all registered badges """

    params: PARAMS = {
        'select': 'name',
    }
    result: JSON = await api_gets(rest_key, 'badge', params)
    return get_names(result)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_get_badge(rest_key: str, name: str) -> JSON:
    """ Get all columns of the badge with `name` """

    return await api_get(rest_key, 'badge', name)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_create_badge(rest_key: str, name: str) -> str:
    """ Register a badge """

    data: DATA = {
        'name': name,
    }
    return await api_create(rest_key, 'badge', data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_delete_badge(rest_key: str, name: str) -> str:
    """ Unregister a badge """

    return await api_delete(rest_key, 'badge', name)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_rename_badge(rest_key: str, name: str, new_name: str) -> str:
    """ Change a badge's name """

    data: DATA = {
        'name': new_name,
    }
    return await api_update(rest_key, 'badge', name, data)

@trace(logger)
@typechecked
async def api_get_badge_id(rest_key: str, name: str) -> int:
    """ Get the `id` of the badge with `name` """

    params: PARAMS = {
        'select': 'id',
    }
    result: JSON = await api_get(rest_key, 'badge', name, params)
    assert len(
        result) == 1, f'api_get_badge() result len should be 1, but it is {len(result)} {result}'
    return int(result[0]['id'])

@logerror(logger)
@trace(logger)
@typechecked
async def api_get_badge_by_id(rest_key: str, badge_id:int) -> JSON:
    """ Get all columns of the badge with `name` """

    params: PARAMS = {
        'select': 'name',
    }
    result: JSON = await api_get_by_id(rest_key, 'badge', str(badge_id), params)
    assert len(
        result) == 1, f'api_get_badge() result len should be 1, but it is {len(result)} {result}'
    return result[0]
