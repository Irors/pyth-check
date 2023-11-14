from sdk import main_check
import loguru

with open('wallets/Aptos-wallets.txt') as apw:
    apw = [row.strip() for row in apw]

with open('wallets/EVM-wallets.txt') as emw:
    emw = [row.strip() for row in emw]

with open('wallets/Solana-wallets.txt') as sow:
    sow = [row.strip() for row in sow]

with open('wallets/Sui-wallets.txt') as suw:
    suw = [row.strip() for row in suw]


if __name__ == '__main__':
    loguru.logger.info('Начинаю парсить')
    main_check(apw, 'aptos')
    main_check(emw, 'evm')
    main_check(sow, 'solana')
    main_check(suw, 'sui')
    loguru.logger.success('Закончил парсить успешно')
