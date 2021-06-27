import telebot
import redis
import json
import asyncio
import time
import os
import base64
from Crypto.Hash import SHA256

import json
import binascii
import requests
from getpass import getpass
from datetime import datetime, timedelta
from ueosio import sign_tx, DataStream, get_expiration, get_tapos_info, build_push_transaction_body

from input import *

# --------------------About Bot--------------------------------------------------------------------
bot= telebot.TeleBot(token= API_key, parse_mode= None)			# You can set parse_mode by default. HTML or 'MARKDOWN'
bot.about = "This is a KYC Bot."
bot.owner = "@abhi3700"

# --------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL, ssl_cert_reqs=None)		# ssl_verify to false

# =========================UTILITY================================
# Calculate the SHA256 hash of any input
def get_hash_sha256(i):
	h = SHA256.new()
	h.update(bytes(i, 'utf-8'))
	empty_hash = h.hexdigest()
	return empty_hash

# =========================func for addmodkyc ACTION========================================================
'''
	@return Returns response
'''
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

# =======================func for delkyc ACTION===================================================================
async def delkyc(
		plat_user_id
	):
	tx = {
			"delay_sec":0,
			"max_cpu_usage_ms":0,
			"actions":[
				{
					"account": kyc_eosio_ac,
					"name": del_action,
					"data":{
						'plat_user_id': plat_user_id,
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

# =======================func for delkyc ACTION===================================================================
async def setviews(
		plat_user_id,
		view_status
	):
	tx = {
			"delay_sec":0,
			"max_cpu_usage_ms":0,
			"actions":[
				{
					"account": kyc_eosio_ac,
					"name": del_action,
					"data":{
						'plat_user_id': plat_user_id,
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

# ===========================command: /start /help===========================================================================
@bot.message_handler(commands=['start', 'help'])
def start_help_command(message):
	'''
	This is a KYC Bot.

	Description: Here, all the KYC info added/modified is first validated on Blockchain & then stored into cloud database. User gets to receive a unique immutable transaction id, which acts as a proof for an activity done.  

	Use these commands to add/modify your KYC info.

	/addmodkyc - Add/Modify KYC to this bot via Blockchain
	/showkycinfo - Show user's updated KYC info on Cloud & Blockchain
	/delkyc - Delete user's KYC info from this bot via Blockchain
	'''
	bot.send_message(message.chat.id, 
		'''
		This is a KYC Bot.

		<u>Description</u>: \nHere, all the KYC info added/modified is first validated on Blockchain & then stored into cloud database. User gets to receive a unique immutable transaction id, which acts as a proof for an activity done.  

		Use these commands to add/modify your KYC info.

		<b>/start</b> - Start the Bot 
		<b>/help</b> - Help
		<b>/addmodkyc</b> - Add/Modify KYC to this bot via Blockchain
		<b>/showkycinfo</b> - Show user's updated KYC info on Cloud & Blockchain
		<b>/delkyc</b> - Delete user's KYC info from this bot via Blockchain
		''',
		parse_mode= 'HTML'
	)

# ===========================command: /showkycinfo===========================================================================
@bot.message_handler(commands=['showkycinfo'])
def showkycinfo_command(message):
	'''
		Show user's updated KYC info 
	'''
	name = address = ''		# initialize all at a time
	try:
		bot.send_message(message.chat.id, 'Please wait...')
		t_start = time.time()
		if r.hexists(str(message.chat.id), 'name') == True:
			name = r.hget(str(message.chat.id), 'name').decode('utf-8')		
		if r.hexists(str(message.chat.id), 'address') == True:
			address = r.hget(str(message.chat.id), 'address').decode('utf-8')

		bot.send_message(message.chat.id, f"<u><b>Your updated KYC info is shown here: </b></u> \n\n- <u>Name:</u> {name} \n- <u>Address</u>: {address}", parse_mode= 'HTML')

		if r.hexists(str(message.chat.id), 'docfront') == True:
			# check if the value is not empty (in bytes)
			if r.hget(str(message.chat.id), 'docfront') != b'':
				img_data = r.hget(str(message.chat.id), 'docfront')			# get the 'base64' encoded image data
				with open(f"img_showf_{message.chat.id}.jpg", "wb") as fh:
					# decode the image as 'base64' encoding type & then write
					fh.write(base64.b64decode(img_data))			
				
				with open(f"img_showf_{message.chat.id}.jpg", 'rb') as photo:
					bot.send_photo(message.chat.id, photo, caption="Document front photo")
				
				os.remove(f"img_showf_{message.chat.id}.jpg")		# delete the file after use
		else:
			bot.send_message(message.chat.id, "Sorry! No <u>Document front</u> photo available.", parse_mode='HTML')

		if r.hexists(str(message.chat.id), 'docback') == True:
			# check if the value is not empty (in bytes)
			if r.hget(str(message.chat.id), 'docback') != b'':
				img_data = r.hget(str(message.chat.id), 'docback')			# get the 'base64' encoded image data
				with open(f"img_showb_{message.chat.id}.jpg", "wb") as fh:
					# decode the image as 'base64' encoding type & then write
					fh.write(base64.b64decode(img_data))			
				
				with open(f"img_showb_{message.chat.id}.jpg", 'rb') as photo:
					bot.send_photo(message.chat.id, photo, caption="Document back photo")
				
				os.remove(f"img_showb_{message.chat.id}.jpg")		# delete the file after use
		else:
			bot.send_message(message.chat.id, "Sorry! No <u>Document back</u> photo available.", parse_mode='HTML')

		if r.hexists(str(message.chat.id), 'selfie') == True:
			# check if the value is not empty (in bytes)
			if r.hget(str(message.chat.id), 'selfie') != b'':
				img_data = r.hget(str(message.chat.id), 'selfie')			# get the 'base64' encoded image data
				with open(f"img_shows_{message.chat.id}.jpg", "wb") as fh:
					# decode the image as 'base64' encoding type & then write
					fh.write(base64.b64decode(img_data))			
				
				with open(f"img_shows_{message.chat.id}.jpg", 'rb') as photo:
					bot.send_photo(message.chat.id, photo, caption="Selfie photo")
				
				os.remove(f"img_shows_{message.chat.id}.jpg")		# delete the file after use
		else:
			bot.send_message(message.chat.id, "Sorry! No <u>Selfie</u> photo available.", parse_mode='HTML')

		elapsed_time = time.time() - t_start
		elapsed_time = '{:.2f}'.format(elapsed_time)

		bot.send_message(message.chat.id, f"In order to add or modify fields in KYC, use /addmodkyc command \n<b>Response time: {elapsed_time} secs</b>", parse_mode='HTML')
		# bot.send_message(message.chat.id, 'To view the KYC data on Blockchain DB, click [here](' + kyc_table_info_url.format(chain_name= chain_name, chat_id=message.chat.id) + ')', parse_mode='MARKDOWN')
	
	except redis.exceptions.ConnectionError as e:
		chat.send(f'Redis Database Connection Error')
	

# ===========================command: /addmodkyc===========================================================================
@bot.message_handler(commands=['addmodkyc'])
def addmodkyc_command(message):
	"""
		Add/Modify KYC to this bot via Blockchain
	"""
	markup = telebot.types.InlineKeyboardMarkup(row_width=2)   # 'one_time_keyboard' hides the keyboard automatically when just after pressing button
	
	itembtn1 = telebot.types.InlineKeyboardButton('Name', callback_data = "kyc_name")
	itembtn2 = telebot.types.InlineKeyboardButton('Address', callback_data= "kyc_address")
	itembtn3 = telebot.types.InlineKeyboardButton('Document front photo', callback_data= "kyc_docfrontimg")
	itembtn4 = telebot.types.InlineKeyboardButton('Document back photo', callback_data= "kyc_docbackimg")
	itembtn5 = telebot.types.InlineKeyboardButton('Selfie photo', callback_data= "kyc_selfie")
	
	markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

	bot.send_message(message.chat.id, "Please, select one option to add KYC", reply_markup= markup)

# --------------------------------callback: kyc_name--------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_name')
def kyc_name_callback(call):
	markup = telebot.types.ForceReply(selective=True)
	msg = bot.send_message(call.message.chat.id, "Please, send your full name. E.g. Peter Bennett", reply_markup= markup)
	'''NOT supported'''
	# msg = bot.edit_message_text( "Please, send your full name. E.g. Peter Bennett", call.message.chat.id, call.message.message_id, reply_markup=markup)
	bot.register_next_step_handler(msg, kncallback)

def kncallback(m):
	if m.text:
		res = addmodkyc(m.chat.id, m.text, get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(""))

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			

			# for Redis DB
			try:
				# t_start = time.time()

				bot.send_message(m.chat.id, 'Saving name to Redis DB...')

				r.hset(str(m.chat.id), 'name', m.text)

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.reply_to(m, f'Field saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.reply_to(m, "Field saved.", parse_mode='MARKDOWN')
				bot.send_message(m.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(m.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")
	else:
		bot.send_message(m.chat.id, "Sorry, the name must be of text type message.")

# -----------------------------callback: kyc_address------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_address')
def kyc_address_callback(call):
	markup = telebot.types.ForceReply(selective=True)
	msg = bot.send_message(call.message.chat.id, "Please, send your address. E.g.\n1504 Liberty St.\nNew York, NY\n10004 USA", reply_markup= markup)
	bot.register_next_step_handler(msg, kacallback)


def kacallback(m):
	if m.text:
		res = addmodkyc(m.chat.id, get_hash_sha256(""), get_hash_sha256(m.text), get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(""))

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			

			# for Redis DB
			try:
				# t_start = time.time()

				bot.send_message(m.chat.id, 'Saving name to Redis DB...')

				r.hset(str(m.chat.id), 'address', m.text)

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.reply_to(m, f'Field saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.reply_to(m, "Field saved.", parse_mode='MARKDOWN')
				bot.send_message(m.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(m.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")
	else:
		bot.send_message(m.chat.id, "Sorry, the address must be of text type message.")
	
# ---------------------------callback: kyc_docfrontimg------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_docfrontimg')
def kyc_docfrontimg_callback(call):
	markup = telebot.types.ForceReply(selective=True)
	msg = bot.send_photo(call.message.chat.id, open("../others/res/id_front.png", "rb"), caption="Please, send your document front image like this", reply_markup=markup)
	bot.register_next_step_handler(msg, kdfcallback)


def kdfcallback(m):
	if m.photo:
		photo_fileid = m.photo[-1].file_id
		# bot.reply_to(m, f"photo msg detected. & the file_id is \n{photo_fileid}")
		# bot.send_photo(m.chat.id, f"{photo_fileid}")

		# get file info & file path
		file_info = bot.get_file(photo_fileid)

		# download from the Telegram server by 
		downloaded_file = bot.download_file(file_info.file_path)

		# with open("new_file.jpg", 'wb') as new_file:				# compressed file, Otherwise use 'png' format
		# Unique file created for each user & delete after use. Otherwise, there will be clash.
		with open(f"img_kycdocf_{m.chat.id}.jpg", 'wb') as new_file:				
			new_file.write(downloaded_file)

		# send the photo which is downloaded first & then saved
		# bot.send_photo(m.chat.id, open(f"img_{m.caption}_{m.chat.id}.jpg", "rb"))				

		# encode the image as 'base64' encoding type
		img_encoded = base64.b64encode(open(f"img_kycdocf_{m.chat.id}.jpg", "rb").read())

		res = addmodkyc(m.chat.id, get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(img_encoded), get_hash_sha256(""), get_hash_sha256(""))

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			

			# for Redis DB
			try:
				# t_start = time.time()

				bot.send_message(m.chat.id, 'Saving name to Redis DB...')

				r.hset(str(m.chat.id), "docfront", img_encoded)

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.reply_to(m, f'Photo saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.reply_to(m, "Photo saved.", parse_mode='MARKDOWN')
				bot.send_message(m.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(m.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")

		os.remove(f"img_kycdocf_{m.chat.id}.jpg")		# delete the file after use

	else:
		bot.send_message(m.chat.id, "Sorry, the document must be of photo type message.")

# ---------------------------callback: kyc_docbackimg------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_docbackimg')
def kyc_docbackimg_callback(call):
	markup = telebot.types.ForceReply(selective=True)
	msg = bot.send_photo(call.message.chat.id, open("../others/res/id_back.png", "rb"), caption="Please, send your document back image like this", reply_markup=markup)
	bot.register_next_step_handler(msg, kdbcallback)

def kdbcallback(m):
	if m.photo:
		photo_fileid = m.photo[-1].file_id
		# bot.reply_to(m, f"photo msg detected. & the file_id is \n{photo_fileid}")
		# bot.send_photo(m.chat.id, f"{photo_fileid}")

		# get file info & file path
		file_info = bot.get_file(photo_fileid)

		# download from the Telegram server by 
		downloaded_file = bot.download_file(file_info.file_path)

		# with open("new_file.jpg", 'wb') as new_file:				# compressed file, Otherwise use 'png' format
		# Unique file created for each user & delete after use. Otherwise, there will be clash.
		with open(f"img_kycdocb_{m.chat.id}.jpg", 'wb') as new_file:				
			new_file.write(downloaded_file)

		# send the photo which is downloaded first & then saved
		# bot.send_photo(m.chat.id, open(f"img_{m.caption}_{m.chat.id}.jpg", "rb"))				

		# encode the image as 'base64' encoding type
		img_encoded = base64.b64encode(open(f"img_kycdocb_{m.chat.id}.jpg", "rb").read())

		res = addmodkyc(m.chat.id, get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(img_encoded), get_hash_sha256(""), get_hash_sha256(""))

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			

			# for Redis DB
			try:
				# t_start = time.time()

				bot.send_message(m.chat.id, 'Saving name to Redis DB...')

				r.hset(str(m.chat.id), "docback", img_encoded)

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.reply_to(m, f'Photo saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.reply_to(m, "Photo saved.", parse_mode='MARKDOWN')
				bot.send_message(m.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(m.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")

		os.remove(f"img_kycdocb_{m.chat.id}.jpg")		# delete the file after use

	else:
		bot.send_message(m.chat.id, "Sorry, the document must be of photo type message.")

# ---------------------------callback: kyc_selfie------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_selfie')
def kyc_selfie_callback(call):
	markup = telebot.types.ForceReply(selective=True)
	msg = bot.send_photo(call.message.chat.id, open("../others/res/selfie.jpg", "rb"), caption="Please, send your selfie like this", reply_markup=markup)
	bot.register_next_step_handler(msg, kscallback)

def kscallback(m):
	if m.photo:
		photo_fileid = m.photo[-1].file_id
		# bot.reply_to(m, f"photo msg detected. & the file_id is \n{photo_fileid}")
		# bot.send_photo(m.chat.id, f"{photo_fileid}")

		# get file info & file path
		file_info = bot.get_file(photo_fileid)

		# download from the Telegram server by 
		downloaded_file = bot.download_file(file_info.file_path)

		# with open("new_file.jpg", 'wb') as new_file:				# compressed file, Otherwise use 'png' format
		# Unique file created for each user & delete after use. Otherwise, there will be clash.
		with open(f"img_kycself_{m.chat.id}.jpg", 'wb') as new_file:				
			new_file.write(downloaded_file)

		# send the photo which is downloaded first & then saved
		# bot.send_photo(m.chat.id, open(f"img_{m.caption}_{m.chat.id}.jpg", "rb"))				

		# encode the image as 'base64' encoding type
		img_encoded = base64.b64encode(open(f"img_kycself_{m.chat.id}.jpg", "rb").read())

		res = addmodkyc(m.chat.id, get_hash_sha256(""), get_hash_sha256(""), get_hash_sha256(img_encoded), get_hash_sha256(""), get_hash_sha256(""))

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			

			# for Redis DB
			try:
				# t_start = time.time()

				bot.send_message(m.chat.id, 'Saving name to Redis DB...')

				r.hset(str(m.chat.id), "selfie", img_encoded)

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.reply_to(m, f'Photo saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.reply_to(m, "Photo saved.", parse_mode='MARKDOWN')
				bot.send_message(m.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(m.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")

		os.remove(f"img_kycself_{m.chat.id}.jpg")		# delete the file after use

	else:
		bot.send_message(m.chat.id, "Sorry, the selfie must be of photo type message.")

# ===========================command: /delkyc===========================
@bot.message_handler(commands=['delkyc'])
def delkyc_command(message):
	"""
		Delete user's KYC info from this bot via Blockchain
	"""
	if r.exists(str(message.chat.id)):
		res = delkyc(m.chat.id)

		# for Blockchain
		if res.status_code == 202:
			bot.send_message(m.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(m.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{res.json()['transaction_id']}", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction			
			try:			# for Redis DB
				# t_start = time.time()

				bot.send_message(message.chat.id, 'Deleting KYC from Redis DB...')

				r.delete(str(message.chat.id))

				# elapsed_time = time.time() - t_start
				# elapsed_time = '{:.2f}'.format(elapsed_time)

				# bot.send_message(message.chat.id, f'Your KYC is deleted. To add, use /addmodkyc command. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.send_message(message.chat.id, f'Your KYC is deleted. To add, use /addmodkyc command.')
				bot.send_message(message.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(message.chat.id, f'Redis Database Connection Error')
		else:
			bot.send_message(m.chat.id, f"Sorry, there is a error related to blockchain:\n{res.json()['error']['details'][0]['message']}\nPlease contact the Bot owner {bot.owner}.")

	else:
		bot.send_message(message.chat.id, "Sorry, there is no KYC found to be deleted. To add, use /addmodkyc command.")

# ===========================command: /setkycviewstatus===========================
@bot.message_handler(commands=['setkycviewstatus'])
def setkycviewstatus_command(message):
	"""
		Show the current KYC Access Status
		- | Change |

		if user_id found on the KYC blockchain:
				- fetch the user_id view_status
				- Show change button
		else:
			print("Sorry, there is no KYC data for the user id.")	
	"""
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)   # 'one_time_keyboard' hides the keyboard automatically when just after pressing button
	itembtn1 = telebot.types.InlineKeyboardButton(f'{paintbrush_emoji} Change', callback_data = "setkycviewstatus_callback")
	markup.add(itembtn1)

	bot.send_message(message.chat.id, "Please, select one option to add KYC", reply_markup= markup)
	# try:			# for Redis DB

	# except redis.exceptions.ConnectionError as e:
	# 	bot.send_message(message.chat.id, f'Redis Database Connection Error')

# ---------------------------callback: kyc_selfie------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'setkycviewstatus_callback')
def setkycviewstatus_callback(call):
	# if user_id found on the KYC blockchain:
	if True:
		pass
	# mkup_reply = types.ReplyKeyboardMarkup(one_time_keyboard= True, row_width=2)
	# itembtn_reply1 = types.KeyboardButton("Yes")
	# itembtn_reply2 = types.KeyboardButton("No")
	# mkup_reply.add(itembtn_reply1, itembtn_reply2)
	# msg = bot.send_message(call.message.chat.id, "Do you want to share KYC data with the admin?", reply_markup= mkup_reply)
	# bot.register_next_step_handler(msg, viewstatus_kb_callback)
	else:
		bot.send_message(call.message.chat.id, "Sorry, there is no KYC data for the user id.")

def viewstatus_kb_callback(m):
	if ((m.text == 'Yes') or (m.text == 'No')):
		pass
		# pass through the blockchain
		# & then store into the cloud
	else:
		bot.send_message(m.chat.id, "Sorry, you have given an invalid View status.")

# ===========================command: /viewuserkyc===========================
@bot.message_handler(commands=['viewuserkyc'])
def viewuserkyc_command(message):
	'''
		- fetch user_id from KYC TABLE on Blockchain
		- if found:
			check for view status of the user
			if true:
				paste /showkycinfo code
			else:
				print("Sorry, the user has not given the access to the admin to view KYC data.")
		- else:
			print("Sorry, there is no KYC data for the user id.")

	'''
	# if user_id found on the KYC blockchain:
	if True:
		# check for view status of the user
		# if true:
		# 	paste /showkycinfo code
		# else:
		# 	print("Sorry, the user has not given the access to the admin to view KYC data.")
		pass
	else:
		bot.send_message(message.chat.id, "Sorry, there is no KYC data for the user id.")
# ================================================MAIN===========================================================================
bot.polling(none_stop= True)			# for Production
# bot.polling()							# for DEBUG