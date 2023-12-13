""" simple utility functions """

from typing import Dict, List

from discord.utils import get
from structlog import get_logger
from typeguard import typechecked

from .log import logargswl, logerror, logres, trace

logger = get_logger()


@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def is_admin(ctx) -> bool:
    """ return whether the command user has the `admin` role """

    # TODO type hints
    admin_role = get(ctx.guild.roles, name='admin')
    result: bool = admin_role in ctx.author.roles
    return result


@logerror(logger)
@trace(logger)
# @logargswl(logger, 1)
# @logres(logger)
@typechecked
async def arg_helper(ctx, n: int) -> List[str]:
    """ Split the command string """

    args: List[str] = ctx.message.content.split()
    cmd: str = args[0]
    args = args[1:]
    if len(args) != n:
        raise ValueError(
            f'Command {cmd} expects {n} argument(s), but you gave {len(args)}: {args}')
    return args


@logerror(logger)
@trace(logger)
@logres(logger)
@typechecked
async def get_arg(ctx) -> str:
    """ Get the argument for a single-argument command """

    # return ctx.message.content.split(maxsplit=1)[1] # Extract the arg from the command message
    args: List[str] = await arg_helper(ctx, 1)
    return args[0]


@logerror(logger)
@trace(logger)
@logargswl(logger, 1)
@logres(logger)
@typechecked
async def get_args(ctx, n: int) -> List[str]:
    """ Get the arguments for an n-argument command """

    # Extract n args from the command message
    # args:List[str] = ctx.message.content.split(maxsplit=n)[1:]
    return await arg_helper(ctx, n)


@typechecked
def get_name(json: Dict[str, str]) -> str:
    """ get the value associated with the `name` key """

    return json['name']


@typechecked
def get_names(json: List[Dict[str, str]]) -> List[str]:
    """ map get_name() over the list """

    return list(map(get_name, json))

@typechecked
def get_id(json: Dict[str, int]) -> int:
    """ get the value associated with the `id` key """

    return json['id']


@typechecked
def get_ids(json: List[Dict[str, int]]) -> List[int]:
    """ map get_id() over the list """

    return list(map(get_id, json))

@typechecked
def get_user_id(json: Dict[str, int]) -> int:
    """ get the value associated with the `user_id` key """

    return json['user_id']


@typechecked
def get_user_ids(json: List[Dict[str, int]]) -> List[int]:
    """ map get_user_id() over the list """

    return list(map(get_user_id, json))

@typechecked
def get_game_id(json: Dict[str, int]) -> int:
    """ get the value associated with the `game_id` key """

    return json['game_id']


@typechecked
def get_game_ids(json: List[Dict[str, int]]) -> List[int]:
    """ map get_game_id() over the list """

    return list(map(get_game_id, json))

@typechecked
def get_remaining(json: Dict[str, int]) -> int:
    """ get the value associated with the `remaining` key """

    return json['remaining']


@typechecked
def get_remainings(json: List[Dict[str, int]]) -> List[int]:
    """ map get_remaining() over the list """

    return list(map(get_remaining, json))

@typechecked
def get_secret(json: Dict[str, str]) -> str:
    """ get the value associated with the `secret` key """

    return json['secret']


@typechecked
def get_secrets(json: List[Dict[str, str]]) -> List[str]:
    """ map get_secret() over the list """

    return list(map(get_secret, json))

@typechecked
def get_badge_id(json: Dict[str, int]) -> int:
    """ get the value associated with the `badge_id` key """

    return json['badge_id']


@typechecked
def get_badge_ids(json: List[Dict[str, int]]) -> List[int]:
    """ map get_badge_id() over the list """

    return list(map(get_badge_id, json))
