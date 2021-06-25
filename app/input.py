API_key = "1893739737:AAFLLNIX9oh5Ezt3P7_NQqVOgy3rhd7NsrU"

# Capture using `$ heroku redis:credentials REDIS_URL -a kyctelbot` from the terminal
REDIS_URL = 'rediss://:pa8320ac09b0e9c0becacc449f1dfa87dda956cf4461e26da1ecb2e58757f2081@ec2-54-156-36-95.compute-1.amazonaws.com:9540'

chain_api_url = 'http://jungle3.cryptolions.io:80'      # Jungle Testnet
chain_name = 'jungle3'
chain_type = 'eos-testnet'
# chain_type = 'eos-mainnet'


# kycteosiobot eosio_ac
kyc_eosio_ac = 'kycteosiobot'
kyc_ac_private_key = '5J5rCnpZZDywDAbpjS3VSocUyZp2GYDcR4ht5VPyFJmDAFhP7o2'
kyc_ac_key_perm = 'active'

# ACTION
addmod_action = 'addmodkyc'
del_action = 'delkyc'

# TABLE
kyc_table_info_url = "https://bloks.io/account/kycteosiobot?loadContract=true&tab=Tables&table=kyc&account=kycteosiobot&scope=kycteosiobot&limit=100&lower_bound={chat_id}&upper_bound={chat_id}" if chain_type== "eos-mainnet" else "https://{chain_name}.bloks.io/account/kycteosiobot?loadContract=true&tab=Tables&table=kyc&account=kycteosiobot&scope=kycteosiobot&limit=100&lower_bound={chat_id}&upper_bound={chat_id}"


# IPFS
API_ENDPOINT = "https://api.nft.storage/upload"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGU0QTRhOTNGQzBlZTI4MjEyMjBiQTI0RTgwNTkxNjg2NzY1QUFCNDMiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTYyMTAyMjY0NDQ1OCwibmFtZSI6Imt5Y2JvdCJ9.rkAqB60ANzkwoe5XGIP89fTrxxiyK4zkIRq6bc5NQ7c" 

# Emoji
paintbrush_emoji = '🖌️'						# b'\xf0\x9f\x96\x8c\xef\xb8\x8f'.decode('utf-8')   U+1F58C