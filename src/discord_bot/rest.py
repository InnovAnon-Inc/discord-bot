""" Low-level REST API operations """

from functools import wraps
from typing import Callable, TypeVar
from urllib.parse import urlencode

from aiohttp import ClientSession
from structlog import get_logger
from typeguard import typechecked

from .log import logargswl, logerror, logres, trace
from .types import DATA, HEADERS, JSON, PARAMS, P

logger = get_logger()


class RestException(Exception):
    """ REST API Exception """

##
# REST API CRUD Helpers
##


@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def rest_encode(base_url: str, params: PARAMS) -> str:
    """ join the `base_url` with the urlencoded params """

    encoded_params: str = urlencode(params)
    return f'{base_url}?{encoded_params}'

RestT = TypeVar('RestT', JSON, str)
CallableApi = Callable[[str, PARAMS, HEADERS, P.args, P.kwargs], RestT]
CallableRest = Callable[[str, ClientSession, HEADERS, P.args, P.kwargs], RestT]
# WrapperRest  = Callable[[CallableRest], CallableApi]

# @logerror(logger) # not async


@typechecked
# @logres(logger) # not async
def rest_params(func: CallableRest) -> CallableApi:
    """
    rewrite the function signature to accept
    the full url and a ClientSession
    """

    @wraps(func)
    async def wrapper(base_url: str, params: PARAMS, *args: P.args, **kwargs: P.kwargs) -> RestT:
        url: str = await rest_encode(base_url, params)
        async with ClientSession() as session:
            return await func(url, session, *args, **kwargs)
    return wrapper


@logerror(logger)
@trace(logger)
@logargswl(logger, 0, 1)  # base_url, params
@logres(logger)
@rest_params  # rewrites siggy
@logargswl(logger, 0)  # url
@typechecked
async def rest_get(
        url: str, session: ClientSession, headers: HEADERS,
        *args: P.args, **kwargs: P.kwargs) -> JSON:
    """ do a `get` operation """

    assert not args, f'rest_get() args should be unused, but it is {args}'
    assert not kwargs, f'rest_get() kwargs should be unused, but it is {kwargs}'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise RestException(
                f"Failed to get. HTTP status code: {response.status}")
        result: JSON = await response.json()
        return result


@logerror(logger)
@trace(logger)
@logargswl(logger, 0, 1)  # base_url, params
@logres(logger)
@rest_params  # rewrites siggy
@logargswl(logger, 0)  # url
@typechecked
async def rest_post(
        url: str, session: ClientSession, headers: HEADERS, data: DATA,
        *args: P.args, **kwargs: P.kwargs) -> str:
    """ do a `post` operation """

    assert not args, f'rest_post() args should be unused, but it is {args}'
    assert not kwargs, f'rest_post() kwargs should be unused, but it is {kwargs}'

    async with session.post(url, headers=headers, json=data) as response:
        if response.status != 201:
            raise RestException(
                f"Failed to post. HTTP status code: {response.status}")
        return await response.text()


@logerror(logger)
@trace(logger)
@logargswl(logger, 0, 1)  # base_url, params
@logres(logger)
@rest_params  # rewrites siggy
@logargswl(logger, 0)  # url
@typechecked
async def rest_delete(
        url: str, session: ClientSession, headers: HEADERS,
        *args: P.args, **kwargs: P.kwargs) -> str:
    """ do a `delete` operation """

    assert not args, f'rest_delete() args should be unused, but it is {args}'
    assert not kwargs, f'rest_delete() kwargs should be unused, but is is {kwargs}'
    async with session.delete(url, headers=headers) as response:
        if response.status != 204:
            raise RestException(
                f"Failed to delete. HTTP status code: {response.status}")
        return await response.text()


@logerror(logger)
@trace(logger)
@logargswl(logger, 0, 1)  # base_url, params
@logres(logger)
@rest_params  # rewrites siggy
@logargswl(logger, 0)  # url
@typechecked
async def rest_patch(
        url: str, session: ClientSession, headers: HEADERS, data: DATA,
        *args: P.args, **kwargs: P.kwargs) -> str:
    """ do a `patch` operation """

    assert not args, f'rest_patch() args should be unused, but it is {args}'
    assert not kwargs, f'rest_patch() kwargs should be unused, but it is {kwargs}'

    async with session.patch(url, headers=headers, json=data) as response:
        if response.status != 204:
            raise RestException(
                f"Failed to patch. HTTP status code: {response.status}")
        return await response.text()
