from os import getenv

from discord import Client, Intents
from structlog import get_logger
from typeguard import typechecked

from .hello import hellomain

logger = get_logger()


@typechecked
async def bot(TOKEN:str)->None:
    client:Client = Client(intents=Intents.default())

    @client.event
    async def on_ready():
        await logger.ainfo('%s has connected to Discord!', client.user)

    return client.run(TOKEN)

@hellomain(logger)
@typechecked
async def main()->None:
    TOKEN:str = getenv('DISCORD_TOKEN')
    return await bot(TOKEN)
