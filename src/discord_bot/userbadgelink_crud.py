""" UserBadgeLink Table CRUD """

from typing import List
from typing import Dict

from structlog import get_logger
from typeguard import typechecked

from .api import api_create, api_gets, ALL_FIELDS, REST_API
from .log import logerror, trace, logargswl
from .types import DATA, HEADERS, JSON, PARAMS
from .user_crud import api_get_user_id
from .badge_crud import api_get_badge_id
from .user_crud import api_get_user_by_id
from .badge_crud import api_get_badge_by_id
from .rest import rest_get, rest_delete, rest_patch
from .util import get_user_ids, get_badge_ids, get_remainings, get_secrets, get_names

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
        user_id: int, badge_id: int,
        params: PARAMS = ALL_FIELDS) -> JSON:
    """ get the row with the specified `name` """

    url: str = '/'.join([REST_API, table])
    params = dict(params)

    assert 'user_id' not in params, f'params should not contain a `user_id` key, but params is {params}'
    params['user_id'] = f'eq.{user_id}'

    assert 'badge_id' not in params, f'params should not contain a `badge_id` key, but params is {params}'
    params['badge_id'] = f'eq.{badge_id}'

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
        user_id: int, badge_id: int) -> str:
    """ do a delete operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'user_id': f'eq.{user_id}',
        'badge_id': f'eq.{badge_id}',
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
        user_id: int, badge_id: int, data: DATA) -> str:
    """ do an update/patch operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'user_id': f'eq.{user_id}',
        'badge_id': f'eq.{badge_id}',
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
async def api_get_userbadgelinks(rest_key: str) -> JSON:
    """ Get the all fields of all registered userbadgelinks """

    #params: PARAMS = {
    #    # 'select': 'name',
    #    'select': 'user_id,badge_id,remaining',
    #}
    result:JSON = await api_gets(rest_key, 'userbadgelink', params)

    user_ids  :List[int] = get_user_ids(result)
    badge_ids  :List[int] = get_badge_ids(result)
    #remainings:List[int] = get_remainings(result)

    #user_names:List[str] = list(map(api_get_user_by_id, user_ids))
    #badge_names:List[str] = list(map(api_get_badge_by_id, badge_ids))
    user_dicts:List[Dict[str,str]] = [await api_get_user_by_id(rest_key, user_id) for user_id in user_ids]
    badge_dicts:List[Dict[str,str]] = [await api_get_badge_by_id(rest_key, badge_id) for badge_id in badge_ids]

    user_names:List[str] = get_names(user_dicts)
    badge_names:List[str] = get_names(badge_dicts)

    rows:List[Dict[str,str]] = [ {
        'user_name': user_name,
        'badge_name': badge_name,
        #'remaining': str(remaining),
    #} for user_name, badge_name, remaining in zip(user_names, badge_names, remainings)]
    } for user_name, badge_name in zip(user_names, badge_names)]
    return rows




@logerror(logger)
@trace(logger)
@typechecked
async def api_get_userbadgelink(rest_key: str, user_name: str, badge_name: str) -> JSON:
    """ Get all columns of the userbadgelink with `user_name` and `badge_name` """

    user_id: int = await api_get_user_id(rest_key, user_name)
    badge_id: int = await api_get_badge_id(rest_key, badge_name)
    result: JSON = await api_get2(rest_key, 'userbadgelink', user_id, badge_id)
    assert len(
        result) == 1, f'api_get_userbadgelink() result len should be 1, but it is {len(result)} {result}'
    return result[0]

# @logerror(logger)


@trace(logger)
@typechecked
async def api_create_userbadgelink(rest_key: str, user_name: str, badge_name: str) -> str:
    """ Register a userbadgelink """

    user_id: int = await api_get_user_id(rest_key, user_name)
    badge_id: int = await api_get_badge_id(rest_key, badge_name)
    data: DATA = {
        'user_id': str(user_id),
        'badge_id': str(badge_id),
    }
    return await api_create(rest_key, 'userbadgelink', data)

# @logerror(logger)


@trace(logger)
@typechecked
async def api_delete_userbadgelink(rest_key: str, user_name: str, badge_name: str) -> str:
    """ Unregister a userbadgelink """

    user_id: int = await api_get_user_id(rest_key, user_name)
    badge_id: int = await api_get_badge_id(rest_key, badge_name)
    return await api_delete2(rest_key, 'userbadgelink', user_id, badge_id)

