""" IA Logging """

from functools import wraps
from typing import Callable, List, Tuple, Union

from typeguard import typechecked

from .types import CallableVarArgs, P, T, Wrapper

WlArgs = Callable[[List[int], P.  args], List[str]]
WlKwArgs = Callable[[List[str], P.kwargs], List[str]]


@typechecked
def trace(logger) -> Wrapper:
    """ Trace the entry and exit """

    @typechecked
    def decorator(func: CallableVarArgs) -> CallableVarArgs:
        # @typechecked
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            await logger.adebug('Enter %s', func.__name__)
            try:
                return await func(*args, **kwargs)
            finally:
                await logger.adebug('Leave %s', func.__name__)
        return wrapper
    return decorator


@typechecked
def logerror(logger, *E: Union[Exception, None]) -> Wrapper:
    """ Log the specified exceptions """

    if not E:
        E = Exception

    @typechecked
    def decorator(func: CallableVarArgs) -> CallableVarArgs:
        # @typechecked
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except E:
                await logger.aexception(f'Error {func.__name__}')
                raise
        return wrapper
    return decorator


@typechecked
def logres(logger) -> Wrapper:
    """ Log the return value """

    @typechecked
    def decorator(func: CallableVarArgs) -> CallableVarArgs:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            res: T = await func(*args, **kwargs)
            await logger.adebug('%s ==> %s', func.__name__, res)
            return res
        return wrapper
    return decorator


@typechecked
def logargswl(logger, *ndxs: int, kwargs: List[str] = []) -> Wrapper:
    """ Log the specified arguments """

    @typechecked
    def decorator(func: CallableVarArgs) -> CallableVarArgs:
        @wraps(func)
        async def wrapper(*fargs: P.args, **fkwargs: P.kwargs) -> T:
            mystr: str = wlstr(ndxs, kwargs, *fargs, **fkwargs)
            await logger.adebug('%s(%s)', func.__name__, mystr)
            return await func(*fargs, **fkwargs)
        return wrapper
    return decorator


@typechecked
def wlstr(ndxs: Tuple[int, ...], kws: List[str], *args: P.args, **kwargs: P.kwargs) -> str:
    """ Filter the specified arguments """

    largs: str = largstr(whitelist_args, ndxs, *args)
    lkwargs: str = lkwargstr(whitelist_kwargs, kws, **kwargs)
    return ','.join([largs, lkwargs])


@typechecked
def largstr(argcb: WlArgs, fargs: Tuple[int, ...], *args: P.args, **_: P.kwargs) -> str:
    """ Comma-separate the arguments """

    assert not _, f'largstr() _ should be unused, but it is {_}'
    return ','.join(argcb(fargs, *args, **_))


@typechecked
def lkwargstr(kwargcb: WlKwArgs, fkwargs: List[str], *_: P.args, **kwargs: P.kwargs) -> str:
    """ Comma-separate the keyword arguments """

    assert not _, f'lkwargstr() _ should be unused, but it is {_}'
    return ','.join(kwargcb(fkwargs, *_, **kwargs))


@typechecked
def whitelist_args(only: Tuple[int, ...], *args: P.args, **_: P.kwargs) -> List[str]:
    """ Get the argument list """

    assert not _, f'whitelist_args() _ should be unused, but it is {_}'
    if only:
        return [f"{arg}" for i, arg in enumerate(args) if i in only]
    return list_args(*args, **_)


@typechecked
def whitelist_kwargs(only: List[str], *_: P.args, **kwargs: P.kwargs) -> List[str]:
    """ Get the keyword argument list """

    assert not _, f'whitelist_kwargs() _ should be unused, but it is {_}'
    if only:
        return [f"{key}={value}" for key, value in kwargs.items() if key in only]
    return list_kwargs(*_, **kwargs)


@typechecked
def list_args(*args: P.args, **_: P.kwargs) -> List[str]:
    """ Get the argument list """

    assert not _, f'list_args() _ should be unused, but it is {_}'
    return [f"{arg}" for arg in args]


@typechecked
def list_kwargs(*_: P.args, **kwargs: P.kwargs) -> List[str]:
    """ Get the keyword argument list """

    assert not _, f'list_kwargs() _ should be unused, but it is {_}'
    return [f"{key}={value}" for key, value in kwargs.items()]


__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, InnovAnon, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
