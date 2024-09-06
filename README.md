# BERA420 Kodiak Faucet Claimer
- Channel: [Mimble Wimble LAB](https://t.me/MimbleWimbleLAB)
- Chat: [Mimble Wimble DAO CHAT](https://t.me/MWDAO_Chat)
- Main Channel: [Mimble Wimble DAO](https://t.me/MimbleWimbleDAO)

An automated tool for claiming BERA tokens from faucet.kodiak.finance.

- 💀 Tested only on macOs.
- 💀 Be careful with the number of threads

## 🚀 Features

- Using selenimbase UC driver
- Automatic CAPTCHA solving
- Multi-threaded account processing
- BERA balance check before claiming attempt
- Automatic replacement of non-working proxies
- Browser data cleanup after each use (optional)

## 🔐 CapMonster Setup

You need CapMonster for CAPTCHA solving. To use this service:

1. Visit [https://capmonster.cloud/Dashboard](https://capmonster.cloud/Dashboard)
2. Create an account or log in if you already have one
3. Obtain your API key from the dashboard
4. Ensure you have sufficient balance in your CapMonster account

Remember to add your CapMonster API key to the `config.py` file. The script will not function correctly without a valid API key and sufficient balance in your CapMonster account.

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/smeshny/bera420kodiakFaucet.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv my_venv
   source my_venv/bin/activate
   ```

3. Navigate to the project directory:
   ```bash
   cd bera420kodiakFaucet
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Data Setup

In the `./data/` folder, set up the following files:

1. **bera_wallets.xlsx**
   - Rename `EXAMPLE_bera_wallets.xlsx` to `bera_wallets.xlsx`
   - Fill the file with your data following the example. Fill adresses, not PK.

2. **config.py**
   - Rename `EXAMPLE_config.py` to `config.py`
   - Fill in the configuration settings (API keys, timeouts, etc.)
   - Set `IS_HEADLESS=False` to watch the process in the browser
   - UTC time used everywhere!

3. **proxies_replacement.txt**
   - Rename `EXAMPLE_proxies_replacement.txt` to `proxies_replacement.txt`
   - Add additional residential proxies (4200 recommended)
   - Every time when proxy changing it will delete this proxy from the end of this file

## 🏃‍♂️ Running the Script

After setting up all files, run the script:

```bash
python main.py
```

## ⚠️ Disclaimer

Use this tool at your own risk. The author is not responsible for any consequences of its use.
