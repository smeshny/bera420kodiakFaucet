# BERA420 Kodiak Faucet Claimer

An automated tool for claiming BERA tokens from faucet.kodiak.finance.

## 🚀 Features

- Using selenimbase UC driver
- Automatic CAPTCHA solving
- Multi-threaded account processing
- BERA balance check before claiming attempt
- Automatic replacement of non-working proxies
- Browser data cleanup after each use (optional)

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/smeshny/bera420kodiakFaucet.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv my_venv
   source my_venv/bin/activate  # For Linux/Mac
   # or
   my_venv\Scripts\activate  # For Windows
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