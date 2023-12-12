from functools import wraps
from sys import version as sysversion

from typeguard import typechecked

from .types import CallableVarArgs
from .types import Wrapper
from .types import T, P
from .version import version

@typechecked
def hellomain(logger)->Wrapper:
    @typechecked
    def decorator(func:CallableVarArgs)->CallableVarArgs:
        @wraps(func)
        async def wrapper(*args:P.args, **kwargs:P.kwargs)->T:
            await logger.ainfo("%s %s (c) 2023 Botze Co.", __name__, version)
            await logger.ainfo("Python %s", sysversion)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

__author__    :str = "AI Assistant"
__copyright__ :str = "Copyright 2023, InnovAnon, Inc."
__license__   :str = "Proprietary"
__version__   :str = "1.0"
__maintainer__:str = "@lmaddox"
__email__     :str = "InnovAnon-Inc@gmx.com"
__status__    :str = "Production"
