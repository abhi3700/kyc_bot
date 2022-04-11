import os
from dotenv import load_dotenv

load_dotenv()  #  take environment variables from .env.

# -------------------------------------------------------------------------------
API_KEY = str(os.getenv('API_KEY'))

# Capture using `$ heroku redis:credentials REDIS_URL -a kyctelbot` from the terminal
REDIS_URL = str(os.getenv('REDIS_URL'))

chain_api_url = 'http://jungle3.cryptolions.io:80'      # Jungle Testnet
chain_name = 'jungle3'
chain_type = 'eos-testnet'
# chain_type = 'eos-mainnet'


# kycteosiobot eosio_ac
kyc_eosio_ac = 'kycteosiobot'
kyc_ac_private_key = str(os.getenv('KYC_AC_PRIVATE_KEY'))
kyc_ac_key_perm = 'active'

# ACTION
addmod_action = 'addmodkyc'
del_action = 'delkyc'
setviews_action = 'setkycviews'

# TABLE
# kyc_table_info_url = "https://bloks.io/account/kycteosiobot?loadContract=true&tab=Tables&table=kyc&account=kycteosiobot&scope=kycteosiobot&limit=100&lower_bound={chat_id}&upper_bound={chat_id}" if chain_type== "eos-mainnet" else "https://{chain_name}.bloks.io/account/kycteosiobot?loadContract=true&tab=Tables&table=kyc&account=kycteosiobot&scope=kycteosiobot&limit=100&lower_bound={chat_id}&upper_bound={chat_id}"

# Emoji
paintbrush_emoji = '🖌️'						# b'\xf0\x9f\x96\x8c\xef\xb8\x8f'.decode('utf-8')   U+1F58C
keyboard_emoji = '⌨️'						# b'\xe2\x8c\xa8\xef\xb8\x8f'.decode('utf-8')	U+2328