import json
import binascii
import requests
from getpass import getpass
from datetime import datetime, timedelta
from ueosio import sign_tx, DataStream, get_expiration, get_tapos_info, build_push_transaction_body
from Crypto.Hash import SHA256


# ======================================================================
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
setviews_action = 'setkycviews'

# ======================================================================
def addmodkyc(
		plat_user_id,
		fullname,
		address_hash,
		document_id_front_hash,
		document_id_back_hash,
		selfie_hash 
	):
	tx = {
			"delay_sec":0,
			"max_cpu_usage_ms":0,
			"actions":[
				{
					"account": kyc_eosio_ac,
					"name": addmod_action,
					"data":{
						'plat_user_id': plat_user_id,
						'fullname': fullname,
						'address_hash': address_hash,
						'document_id_front_hash': document_id_front_hash,
						'document_id_back_hash': document_id_back_hash,
						'selfie_hash': selfie_hash
						},
					"authorization":[{"actor":kyc_eosio_ac,"permission": kyc_ac_key_perm}]
				}
			]
		}

	# Get chain info from a working api node
	info = requests.get(f'{chain_api_url}/v1/chain/get_info').json()
	ref_block_num, ref_block_prefix = get_tapos_info(info['last_irreversible_block_id'])
	chain_id = info['chain_id']

	# package transaction
	data = tx['actions'][0]['data']
	ds = DataStream()
	ds.pack_uint64(data['plat_user_id'])
	ds.pack_string(data['fullname'])
	ds.pack_checksum256(data['address_hash'])
	ds.pack_checksum256(data['document_id_front_hash'])
	ds.pack_checksum256(data['document_id_back_hash'])
	ds.pack_checksum256(data['selfie_hash'])

	tx['actions'][0]['data'] = binascii.hexlify(ds.getvalue()).decode('utf-8')

	tx.update({
		"expiration": get_expiration(datetime.utcnow(), timedelta(minutes=15).total_seconds()),
		"ref_block_num": ref_block_num,
		"ref_block_prefix": ref_block_prefix,
		"max_net_usage_words": 0,
		"max_cpu_usage_ms": 0,
		"delay_sec": 0,
		"context_free_actions": [],
		"transaction_extensions": [],
		"context_free_data": []
	})

	# Sign transaction
	tx_id, tx = sign_tx(
	   chain_id,
	   tx,
	   kyc_ac_private_key
	)
	ds = DataStream()
	ds.pack_transaction(tx)
	packed_trx = binascii.hexlify(ds.getvalue()).decode('utf-8')
	tx = build_push_transaction_body(tx['signatures'][0], packed_trx)

	# Push transaction
	res = requests.post(f'{chain_api_url}/v1/chain/push_transaction', json=tx)

	return res


def setviews(
		plat_user_id,
		view_status
	):
	tx = {
			"delay_sec":0,
			"max_cpu_usage_ms":0,
			"actions":[
				{
					"account": kyc_eosio_ac,
					"name": setviews_action,
					"data":{
						'plat_user_id': plat_user_id,
						'view_status': view_status
						},
					"authorization":[{"actor":kyc_eosio_ac,"permission": kyc_ac_key_perm}]
				}
			]
		}

	# Get chain info from a working api node
	info = requests.get(f'{chain_api_url}/v1/chain/get_info').json()
	ref_block_num, ref_block_prefix = get_tapos_info(info['last_irreversible_block_id'])
	chain_id = info['chain_id']

	# package transaction
	data = tx['actions'][0]['data']
	ds = DataStream()
	ds.pack_uint64(data['plat_user_id'])
	ds.pack_bool(data['view_status'])

	tx['actions'][0]['data'] = binascii.hexlify(ds.getvalue()).decode('utf-8')

	tx.update({
		"expiration": get_expiration(datetime.utcnow(), timedelta(minutes=15).total_seconds()),
		"ref_block_num": ref_block_num,
		"ref_block_prefix": ref_block_prefix,
		"max_net_usage_words": 0,
		"max_cpu_usage_ms": 0,
		"delay_sec": 0,
		"context_free_actions": [],
		"transaction_extensions": [],
		"context_free_data": []
	})

	# Sign transaction
	tx_id, tx = sign_tx(
	   chain_id,
	   tx,
	   kyc_ac_private_key
	)
	ds = DataStream()
	ds.pack_transaction(tx)
	packed_trx = binascii.hexlify(ds.getvalue()).decode('utf-8')
	tx = build_push_transaction_body(tx['signatures'][0], packed_trx)

	# Push transaction
	res = requests.post(f'{chain_api_url}/v1/chain/push_transaction', json=tx)

	return res

# ==============================================
# Calculate the SHA256 hash of any input
def get_hash_sha256(i):
	h = SHA256.new()
	h.update(bytes(i, 'utf-8'))
	empty_hash = h.hexdigest()
	return empty_hash


# ==============================================
# Main function
if __name__ == '__main__':
	empty_hash = get_hash_sha256('')
	# h = SHA256.new()
	# h.update(bytes('', 'utf-8'))
	# empty_hash = h.hexdigest()

	# res = addmodkyc(3214324, "Abhijit Roy" , empty_hash, empty_hash, empty_hash, empty_hash)
	# if res.status_code == 202:
	# 	print(res.json()['transaction_id'])
	# else:
	# 	print(res.json()['error']['details'][0]['message'])


	res = setviews(3214324, 0)
	if res.status_code == 202:
		print(res.json()['transaction_id'])
	else:
		print(res.json()['error']['details'][0]['message'])


