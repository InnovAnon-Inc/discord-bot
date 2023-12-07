from os import getenv

from discord import Intents
from discord import Message
from discord.ext.commands import Bot
from discord.utils import setup_logging
from discord.utils import find
from discord import Member
from structlog import get_logger
from typeguard import typechecked

from .hello import hellomain
from .types import P

logger = get_logger()
setup_logging()

@typechecked
async def bot(token:str, guild:str)->None:
    intents:Intents = Intents.default()
    bot:Bot = Bot(intents=intents, command_prefix='!')
    
    @bot.event
    @typechecked
    async def on_ready()->None:
        await logger.ainfo('%s has connected to Discord!', bot.user.name)

    @bot.command(name='99')
    @typechecked
    async def nine_nine(ctx)->None:
        brooklyn_99_quotes:List[str] = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        response:str = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    return await bot.start(token)

@hellomain(logger)
@typechecked
async def main()->None:
    TOKEN:str = getenv('DISCORD_TOKEN')
    GUILD:str = getenv('DISCORD_GUILD')
    return await bot(TOKEN, GUILD)
