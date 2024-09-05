import random
import time
import shutil

from seleniumbase import SB

from utils.custom_logger import logger
from utils.account_manager import AccountManager
from utils.proxy_handler import ProxyChecker
from utils.js_simulations import simulaion_mouse_move, simulaion_mouse_move_and_click
from data.config import SLEEP_BETWEEN_ACCOUTNS, ACCOUNTS_FILE, ACCOUTNS_TO_WORK, ACCOUTNS_SHUFFLE, \
                        IS_HEADLESS, CAPMONSTER_API_KEY, CAPTCHA_TIMEOUT, ATTEMPTS_TO_CLICK, \
                        CLEAN_PERSISTENT_DATA, PROXY_TIMEOUT_FOR_CHECKER


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
        logger.error(f"🙀 Can't solve captcha in {CAPTCHA_TIMEOUT} sec.")
        logger.error(e)
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

def check_proxy(input_proxy):
    replacement_file = "./data/proxies_replacement.txt"
    url = "https://www.faucet.kodiak.finance/"

    checker = ProxyChecker(replacement_file)
    
    working_proxy = checker.check_and_replace_proxy(input_proxy, url)

    if working_proxy:
        logger.debug(f"Original proxy is good. Timeout < {PROXY_TIMEOUT_FOR_CHECKER}s")
        if working_proxy != input_proxy:
            logger.debug(f"Original proxy was replaced with a working one from the replacement file.")
            logger.debug(f"New proxy is: {working_proxy}")
        return working_proxy
    else:
        logger.debug(f"No working proxy found for replacement.")


@logger.catch
def main() -> None:
    account_manager = AccountManager(ACCOUNTS_FILE)
    accounts = account_manager.get_accounts(ACCOUTNS_TO_WORK, shuffle=ACCOUTNS_SHUFFLE)
    accounts_in_work = [account['account_name'] for account in accounts]
    logger.debug(f"Start working with {len(accounts_in_work)} accounts in order: {accounts_in_work}")

    for account in accounts:
        account_name, evm_wallet, proxy = account.values()
        logger.debug(f"🤖 Start working with account: {account_name} | {evm_wallet} | Proxy: {proxy}.")

        try:
            working_proxy = check_proxy(proxy)
            open_SB_for_account(account_name, working_proxy, evm_wallet)
        except Exception as e:
            logger.error(e)
            continue
        
        if CLEAN_PERSISTENT_DATA:
            time.sleep(5)
            shutil.rmtree(f"./persistent_data/{account_name}")
            logger.debug(f"Persistent data cleaned for account: {account_name}")
        
        sleep_btw_accs = random.uniform(*SLEEP_BETWEEN_ACCOUTNS)
        logger.debug(f"Start sleeping for {sleep_btw_accs} sec")
        time.sleep(sleep_btw_accs)
            

if __name__ == "__main__":
    main()
