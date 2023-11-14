import asyncio

import loguru
import requests
import aiohttp

def lower(wallet: str) -> str:
    return wallet.lower()

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
    for address in wallets:
        tasks.append(asyncio.create_task(reqst(address, ecosystem)))

    await asyncio.gather(*tasks)

def main_check(wallets: list):
    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        match len(wallets[0]):

            case 66: # SUI
                loguru.logger.info('Sui...')
                loop.run_until_complete(get_eligible(wallets=wallets, ecosystem='sui'))

            case 44: # Solana
                loguru.logger.info('Solana...')
                loop.run_until_complete(get_eligible(wallets=wallets, ecosystem='solana'))

            case 42: # EVM
                loguru.logger.info('EVM...')
                loop.run_until_complete(get_eligible(wallets=wallets, ecosystem='evm'))

        loop.close()

    except Exception as e:
        print('Проблема с указанием кошелька(ов)')