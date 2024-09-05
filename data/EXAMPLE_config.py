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
SLEEP_BETWEEN_ACCOUTNS = (1, 5)

IS_HEADLESS = False

PROXY_TIMEOUT_FOR_CHECKER = 3
CAPTCHA_TIMEOUT = 180
ATTEMPTS_TO_CLICK = 5

CLEAN_PERSISTENT_DATA = True

CAPMONSTER_API_KEY= "" # https://capmonster.cloud/Dashboard

SEND_NOTIFICATIONS = False
TG_TOKEN = '' # https://t.me/BotFather
TG_ID = '132081081' # https://t.me/getmyid_bot