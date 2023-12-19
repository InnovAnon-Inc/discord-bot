""" Low-level Supabase API operations """


from structlog import get_logger
from typeguard import typechecked

from .log import logargswl, logerror, trace
from .rest import rest_delete, rest_get, rest_patch, rest_post
from .types import DATA, HEADERS, JSON, PARAMS

logger = get_logger()

REST_API: str = 'https://byyokbedkfrhtftkqawp.supabase.co/rest/v1'
ALL_FIELDS: PARAMS = {
    'select': '*',
}


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, name
@typechecked
async def api_gets(rest_key: str, table: str, params: PARAMS = ALL_FIELDS) -> JSON:
    """ do a get operation """

    url: str = '/'.join([REST_API, table])
    # params:PARAMS = {
    #    'select': '*',
    # }
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    return await rest_get(url, params, headers)


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, name
@typechecked
async def api_get(rest_key: str, table: str, name: str, params: PARAMS = ALL_FIELDS) -> JSON:
    """ get the row with the specified `name` """

    url: str = '/'.join([REST_API, table])
    # params:PARAMS = {
    #    'name': f'eq.{name}',
    #    'select': '*',
    # }
    assert 'name' not in params, f'params should not contain a `name` key, but params is {params}'
    params = dict(params)
    params['name'] = f'eq.{name}'
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
async def api_get_by_id(rest_key: str, table: str, name: str, params: PARAMS = ALL_FIELDS) -> JSON:
    """ get the row with the specified `id` """

    url: str = '/'.join([REST_API, table])
    # params:PARAMS = {
    #    'id': f'eq.{id}',
    #    'select': '*',
    # }
    assert 'id' not in params, f'params should not contain a `id` key, but params is {params}'
    params = dict(params)
    params['id'] = f'eq.{name}'
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
    }
    result: JSON = await rest_get(url, params, headers)
    return result


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, data
@typechecked
async def api_create(rest_key: str, table: str, data: DATA) -> str:
    """ do a create/post operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {}
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_post(url, params, headers, data)


@logerror(logger)
@trace(logger)
@logargswl(logger, 1, 2)  # table, name
@typechecked
async def api_delete(rest_key: str, table: str, name: str) -> str:
    """ do a delete operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'name': f'eq.{name}',
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
async def api_update(rest_key: str, table: str, name: str, data: DATA) -> str:
    """ do an update/patch operation """

    url: str = '/'.join([REST_API, table])
    params: PARAMS = {
        'name': f'eq.{name}',
    }
    headers: HEADERS = {
        'apikey': rest_key,
        'Authorization': f'Bearer {rest_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
    }
    return await rest_patch(url, params, headers, data)
