import asyncio
from loguru import logger
from sys import stderr
import aiohttp


def add_logger():
    logger.remove()
    logger.add(stderr, format="<bold><blue>{time:HH:mm:ss}</blue> | <level>{level}</level> | <level>{message}</level></bold>")


async def reqst(address: str, ecosystem: str):
    with open('result/result-pyth.txt', 'a') as file:

        async with aiohttp.ClientSession() as session:
            params = {
                'identity': address,
            }

            await session.get(f'https://airdrop.pyth.network/api/grant/v1/{ecosystem}_breakdown', params=params)

            params = {
                'ecosystem': ecosystem,
                'identity': address,
            }

            response = await session.get('https://airdrop.pyth.network/api/grant/v1/amount_and_proof', params=params)
            if response.status == 200:
                file.write(f'{address}\n')

    file.close()


async def get_eligible(wallets: list, ecosystem: str) -> bool:

    tasks = []
    logger.info(f'Найдено {len(wallets)} кошельков | {ecosystem}')
    for address in wallets:
        tasks.append(asyncio.create_task(reqst(address, ecosystem)))

    await asyncio.gather(*tasks)

def main_check(wallets: list, ecosystem: str):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(get_eligible(wallets=wallets, ecosystem=ecosystem))
        loop.close()

    except IndexError:
        pass

    except:
        logger.error('Проблема с указанием кошелька(ов)')