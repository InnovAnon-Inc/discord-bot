from typing import ParamSpec
from typing import Any
from typing import List
from typing import TypeVar
from typing import Tuple
from typing import Dict
from typing import Callable
from typing import Union
from typing import Optional

T = TypeVar('T')
P = ParamSpec('P')

CallableVarArgs = Callable[P,T]
Wrapper         = Callable[[CallableVarArgs],CallableVarArgs]

SettingArg   = Tuple[str,...]
SettingKwArg = Dict[str,str]
CallableSettings = Callable[[SettingArg,SettingKwArg,P.args,P.kwargs],T]

#CallablePool = Callable[[Pool,P.args,P.kwargs],T]
#WrapperPool  = Callable[[CallablePool],CallablePool]

#CallableConn = Callable[[Connection,P.args,P.kwargs],T]
#WrapperConn  = Callable[[CallableConn],CallableConn]

#CallableCurs = Callable[[Cursor,P.args,P.kwargs],T]
#WrapperCurs  = Callable[[CallableCurs],CallableCurs]

#CallableFlask = Callable[P, Flask]
#CallableNone  = Callable[P,None]
#WrapperFlask  = Callable[[CallableFlask, P.args, P.kwargs], CallableNone]

JSON    = Union[List[Dict[str,Any]],Dict[str,Any]]#,str]
HEADERS = Dict[str,str]
DATA    = Dict[str,str]
PARAMS  = Dict[str,str]
