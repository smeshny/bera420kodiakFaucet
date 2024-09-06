import random
import time
import os
import shutil

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from seleniumbase import SB

from utils.custom_logger import logger
from utils.account_manager import AccountManager
from utils.timestamp_helper import save_timestamp, read_timestamp, seconds_from_last_run
from utils.web3_helper import check_BERA_balance
from utils.proxy_handler import ProxyChecker
from utils.js_simulations import simulaion_mouse_move, simulaion_mouse_move_and_click
from data.config import SLEEP_BETWEEN_ACCOUTNS, ACCOUNTS_FILE, ACCOUTNS_TO_WORK, ACCOUTNS_SHUFFLE, \
                        IS_HEADLESS, CAPMONSTER_API_KEY, CAPTCHA_TIMEOUT, ATTEMPTS_TO_CLICK, \
                        CLEAN_PERSISTENT_DATA, PROXY_TIMEOUT_FOR_CHECKER, TREAD_POOL_WORKERS, \
                        NEXT_RUN_WAITING


SUCCESS_WALLETS = []
ALREADY_CLAIMED_WALLETS = []
MORE_THAN_1_BERA_WALLETS = []


@logger.catch
def claim_bera_kodiak(sb: SB, evm_wallet) -> None:
    # install capmonster chrome ext
    capmonster_ext_url = 'chrome-extension://pabjfbciaedomjjfelfafejkppknjleh/popup.html'
    sb.uc_open_with_reconnect(capmonster_ext_url, 1)
    sb.type('//*[@id="client-key-input"]', CAPMONSTER_API_KEY)
    sb.click('//*[@id="client-key-save-btn"]')

    # open faucet
    url = "https://www.faucet.kodiak.finance/"
    sb.uc_open_with_reconnect(url, 6)

    # check if already calimed from this adress or IP
    try:
        sb.sleep(5)
        sb.wait_for_element('div:contains("Congratulations")')
        sb.highlight('div:contains("Congratulations")')
        logger.info(f"👀 Already claimed BERA for wallet: {evm_wallet}")
        if evm_wallet not in ALREADY_CLAIMED_WALLETS:
            ALREADY_CLAIMED_WALLETS.append(evm_wallet)
        return
    except Exception as e:
        if "was not present" in str(e):
            pass
        else:
            logger.error(e)
    
    # Waiting for captcha solve by extension
    try:
        logger.debug(f"Waiting for CAPTCHA solving by extension! Max timeout is {CAPTCHA_TIMEOUT}")
        sb.wait_for_element_clickable('//*[@id="root"]/div/div/div[2]/button', timeout=CAPTCHA_TIMEOUT)
    except Exception as e:
        logger.debug(f"🙀 Can't solve captcha in {CAPTCHA_TIMEOUT} sec.")
        return
    
    sb.sleep(random.uniform(1,3))

    sb.type('//*[@id="root"]/div/div/div[2]/input', evm_wallet)
    sb.sleep(random.uniform(1,2))

    # try to custom JS click drip button
    for attempt in range(1, ATTEMPTS_TO_CLICK + 1):
        logger.debug(f"Attempting to click drip button. {attempt} attempt")
        try:

            sb.highlight('//*[@id="root"]/div/div/div[2]/button')
            sb.sleep(random.uniform(1,2))
            # custom JS mouse moves
            sb.execute_script(simulaion_mouse_move)
            sb.execute_script(simulaion_mouse_move_and_click)
            
            sb.sleep(random.uniform(0.1,0.3))
            sb.sleep(random.uniform(3,5))

        except Exception as e:
            if "was not present" in str(e):
                pass
            else:
                logger.error(e)
                sb.sleep(random.uniform(1, 3))

        sb.sleep(random.uniform(3,5))
        
        try:
            sb.wait_for_element('div:contains("Congratulations")')
            sb.highlight('div:contains("Congratulations")')
            logger.success(f"🫡 🦾 1 BERA claimed for wallet: https://bartio.beratrail.io/address/{evm_wallet}")
            if evm_wallet not in SUCCESS_WALLETS:
                SUCCESS_WALLETS.append(evm_wallet)
            return
        except Exception as e:
            if "was not present" in str(e):
                pass
            else:
                logger.error(e)


@logger.catch
def open_SB_for_account(account_name, proxy, evm_wallet) -> None:

    with SB(
        uc=True, 
        user_data_dir='persistent_data/' + account_name,
        extension_dir='capmonster_chrome_ext/pabjfbciaedomjjfelfafejkppknjleh/1.11.16_0',
        proxy=proxy,
        headless=IS_HEADLESS,
        ) as sb:
    
            claim_bera_kodiak(sb, evm_wallet)


@logger.catch
def check_proxy(input_proxy):
    replacement_file = "./data/proxies_replacement.txt"
    url = "https://www.faucet.kodiak.finance/"

    checker = ProxyChecker(replacement_file)
    
    working_proxy = checker.check_and_replace_proxy(input_proxy, url)

    if working_proxy:
        if working_proxy != input_proxy:
            logger.debug(f"Original proxy was replaced with a working one from the replacement file.")
            logger.debug(f"New proxy is: {working_proxy}")
        else:
            logger.debug(f"Original proxy is good. Timeout < {PROXY_TIMEOUT_FOR_CHECKER}s")
        return working_proxy
    else:
        logger.debug(f"No working proxy found for replacement.")


def clean_persistent_data(account_name: str) -> None:
    if CLEAN_PERSISTENT_DATA:
        if os.path.exists(f"./persistent_data/{account_name}"):
            if os.path.isdir(f"./persistent_data/{account_name}"):
                time.sleep(5)
                shutil.rmtree(f"./persistent_data/{account_name}")
                logger.debug(f"Persistent data cleaned for account: {account_name}")


#threading
# Global
total_accounts = 0
progress_lock = threading.Lock()

@logger.catch
def process_account(account, index):
    account_name, evm_wallet, proxy = account.values()
    
    time.sleep(random.uniform(*SLEEP_BETWEEN_ACCOUTNS))
    
    try:
        working_proxy = check_proxy(proxy)
        if check_BERA_balance(evm_wallet, working_proxy) > 1:
            logger.debug(f"BERA balance > 1 account: {account_name}. Will skip this account")
            if evm_wallet not in MORE_THAN_1_BERA_WALLETS:
                MORE_THAN_1_BERA_WALLETS.append(evm_wallet)
        else:
            open_SB_for_account(account_name, working_proxy, evm_wallet)
    except Exception as e:
        logger.error(f"Error processing account {account_name}: {e}")
    
    with progress_lock:
        clean_persistent_data(account_name)

        logger.debug(f"Completed account: {account_name}.")


@logger.catch
def main() -> None:
    SUCCESS_WALLETS.clear()
    ALREADY_CLAIMED_WALLETS.clear()
    MORE_THAN_1_BERA_WALLETS.clear()
    
    global total_accounts
    account_manager = AccountManager(ACCOUNTS_FILE)
    accounts = account_manager.get_accounts(ACCOUTNS_TO_WORK, shuffle=ACCOUTNS_SHUFFLE)
    accounts_in_work = [account['account_name'] for account in accounts]
    total_accounts = len(accounts_in_work)
    
    logger.debug(f"Start working with {total_accounts} accounts in order: {accounts_in_work}")

    with ThreadPoolExecutor(max_workers=TREAD_POOL_WORKERS) as executor:
        futures = [executor.submit(process_account, account, i) for i, account in enumerate(accounts)]
        
        
        for _ in tqdm(as_completed(futures), total=total_accounts, desc="Processing accounts"):
            pass
    
    logger.success(f"First iteration COMPLETE. Start to work with unseccessfull accounts 💨 🚬")
    
    # REWORK for accounts with errors:
    rework_accounts = [
        account for account in accounts 
        if account['evm_wallet'] not in SUCCESS_WALLETS and 
           account['evm_wallet'] not in ALREADY_CLAIMED_WALLETS and 
           account['evm_wallet'] not in MORE_THAN_1_BERA_WALLETS
    ]
    
    total_rework_accounts = len(rework_accounts)
    logger.success(f"Accounts to REWORK: {total_rework_accounts} 💨 🚬")
    
    with ThreadPoolExecutor(max_workers=TREAD_POOL_WORKERS) as executor:
        futures = [executor.submit(process_account, account, i) for i, account in enumerate(rework_accounts)]
        
        
        for _ in tqdm(as_completed(futures), total=total_rework_accounts, desc="Processing accounts"):
            pass
    
    
    unkonwn_error_wallets_count = len(accounts) - \
                            len(SUCCESS_WALLETS) - \
                            len(ALREADY_CLAIMED_WALLETS) - \
                            len(MORE_THAN_1_BERA_WALLETS)
    
    logger.success(
        f"""
        🫡 JOB DONE! 🫡
        
        Summary:
        • Successful accounts💨 🚬: {len(SUCCESS_WALLETS)} accounts with claimed BERA 💨 🚬
        • Already claimed 👀 in 3H period accounts: {len(ALREADY_CLAIMED_WALLETS)}
        • Accounts > 1 BERA (can't claim on faucet): {len(MORE_THAN_1_BERA_WALLETS)}
        • Accounts with uncknown errors: {unkonwn_error_wallets_count}
        • Total accounts completed: {len(accounts)} 💨 🚬
        """
    )


if __name__ == "__main__":
    while True:
        if seconds_from_last_run() > NEXT_RUN_WAITING:
            logger.success(f"Start new cycle for claiming 💨 🚬")
            main()
            save_timestamp()
            logger.success(f"New claiming cycle will start in {NEXT_RUN_WAITING}s. 💨 🚬")
        else:
            time_remain_to_start = NEXT_RUN_WAITING - seconds_from_last_run()
            logger.debug(f"New claiming cycle will start in {int(time_remain_to_start)}s. 💨 🚬")
            time.sleep(420)