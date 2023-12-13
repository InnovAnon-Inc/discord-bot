""" IA Typing """

from typing import (Any, Callable, Dict, List, ParamSpec, Tuple,
                    TypeVar, Union)

T = TypeVar('T')
P = ParamSpec('P')

CallableVarArgs = Callable[P, T]
Wrapper = Callable[[CallableVarArgs], CallableVarArgs]

SettingArg = Tuple[str, ...]
SettingKwArg = Dict[str, str]
CallableSettings = Callable[[SettingArg, SettingKwArg, P.args, P.kwargs], T]

# CallablePool = Callable[[Pool,P.args,P.kwargs],T]
# WrapperPool  = Callable[[CallablePool],CallablePool]

# CallableConn = Callable[[Connection,P.args,P.kwargs],T]
# WrapperConn  = Callable[[CallableConn],CallableConn]

# CallableCurs = Callable[[Cursor,P.args,P.kwargs],T]
# WrapperCurs  = Callable[[CallableCurs],CallableCurs]

# CallableFlask = Callable[P, Flask]
# CallableNone  = Callable[P,None]
# WrapperFlask  = Callable[[CallableFlask, P.args, P.kwargs], CallableNone]

JSON = Union[List[Dict[str, Any]], Dict[str, Any]]  # ,str]
HEADERS = Dict[str, str]
DATA = Dict[str, str]
PARAMS = Dict[str, str]

__author__: str = "AI Assistant"
__copyright__: str = "Copyright 2023, InnovAnon, Inc."
__license__: str = "Proprietary"
__version__: str = "1.0"
__maintainer__: str = "@lmaddox"
__email__: str = "InnovAnon-Inc@gmx.com"
__status__: str = "Production"
