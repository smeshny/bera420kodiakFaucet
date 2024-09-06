ACCOUNTS_FILE = "data/bera_wallets.xlsx"

"""
        # Get all accounts:
        ACCOUTNS_TO_WORK = []
        # Get specific accounts 1, 5, 7, 8, 9, 10, 11:
        ACCOUTNS_TO_WORK = [1, 5, "7-11"]
        # Get accounts range 7, 8, 9, 10, 11:
        ACCOUTNS_TO_WORK = ["7-11"]
        # Get few ranges 7, 8, 9, 10, 11, 42, 43, 44:
        ACCOUTNS_TO_WORK = ["7-11", "42-44"]
 """
ACCOUTNS_TO_WORK = []
ACCOUTNS_SHUFFLE = True
SLEEP_BETWEEN_ACCOUTNS = (3, 7)
TREAD_POOL_WORKERS = 3 # ☠️☠️☠️ !!! USE THIS VERY CAREFUL!!! . Only with IS_HEADLESS = True.

NEXT_RUN_WAITING = 3 * 60 * 60 # In seconds, Faucet working every 3 HOURS. Script use UTC time.

IS_HEADLESS = True

PROXY_TIMEOUT_FOR_CHECKER = 2
CAPTCHA_TIMEOUT = 66
ATTEMPTS_TO_CLICK = 5

CLEAN_PERSISTENT_DATA = True

CAPMONSTER_API_KEY=""
SEND_NOTIFICATIONS = False
TG_TOKEN = ''
TG_ID = ''