import telebot
import redis
import json
import asyncio
import time
import os
import base64
from Crypto.Hash import SHA256
# import requests

from aioeos import EosAccount, EosJsonRpc, EosTransaction
from aioeos import types

from aioeos.exceptions import EosRpcException
from aioeos.exceptions import EosAccountDoesntExistException
from aioeos.exceptions import EosAssertMessageException
from aioeos.exceptions import EosDeadlineException
from aioeos.exceptions import EosRamUsageExceededException
from aioeos.exceptions import EosTxCpuUsageExceededException
from aioeos.exceptions import EosTxNetUsageExceededException

from input import *

# --------------------About Bot--------------------------------------------------------------------
bot= telebot.TeleBot(token= API_key, parse_mode= None)			# You can set parse_mode by default. HTML or 'MARKDOWN'
bot.about = "This is a KYC Bot."
bot.owner = "@abhi3700"

# --------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL, ssl_cert_reqs=None)		# ssl_verify to false

# =========================func for addmodkyc ACTION========================================================
async def addmodkyc(
		plat_user_id,
		fullname,
		address_hash,
		document_id_front_hash,
		document_id_back_hash,
		selfie_hash,
		message
	):
	t_start = time.time()		# timer start

	contract_account = EosAccount(
	  name=kyc_eosio_ac,
	  private_key=kyc_ac_private_key
	)

	action = types.EosAction(
		account=kyc_eosio_ac,
		name=addmod_action,
		authorization=[contract_account.authorization(kyc_ac_key_perm)],
		data={
			'plat_user_id': plat_user_id,
			'fullname': fullname,
			'address_hash': address_hash,
			'document_id_front_hash': document_id_front_hash,
			'document_id_back_hash': document_id_back_hash,
			'selfie_hash': selfie_hash
		}
	)

	rpc = EosJsonRpc(url=Chain_URL)
	block = await rpc.get_head_block()

	transaction = EosTransaction(
	  ref_block_num=block['block_num'] & 65535,
	  ref_block_prefix=block['ref_block_prefix'],
	  actions=[action]
	)

	response = await rpc.sign_and_push_transaction(
	  transaction, keys=[contract_account.key]
	)
	# bot.send_message(f'{response}')             # print the full response after SUCCESS
	
	response = str(response).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
	# print(response)               # print the full response after replacing single with double quotes
	'''
		Here, as the response o/p is not a valid JSON giving error like this:
		Error:
			Parse error on line 1:
			...producer_block_id": None, "receipt": {"s
			-----------------------^
			Expecting 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '[', got 'undefined'

		So, capture txn_id by char no. i.e. {"transaction_id": "14e310c6e296560202ec808139d7e1b06901616f35b5c4a36ee0a4f065ec72a6"
	'''
	elapsed_time = time.time() - t_start
	elapsed_time = '{:.2f}'.format(elapsed_time)

	bot.send_message(message.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(message.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction

# =======================func for delkyc ACTION===================================================================
async def delkyc(
		plat_user_id,
		message
	):
	t_start = time.time()		# timer start

	contract_account = EosAccount(
	  name=kyc_eosio_ac,
	  private_key=kyc_ac_private_key
	)

	action = types.EosAction(
		account=kyc_eosio_ac,
		name=del_action,
		authorization=[contract_account.authorization(kyc_ac_key_perm)],
		data={
			'plat_user_id': plat_user_id,
		}
	)

	rpc = EosJsonRpc(url=Chain_URL)
	block = await rpc.get_head_block()

	transaction = EosTransaction(
	  ref_block_num=block['block_num'] & 65535,
	  ref_block_prefix=block['ref_block_prefix'],
	  actions=[action]
	)

	response = await rpc.sign_and_push_transaction(
	  transaction, keys=[contract_account.key]
	)
	# chat.send(f'{response}')             # print the full response after SUCCESS
	
	response = str(response).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
	# print(response)               # print the full response after replacing single with double quotes
	'''
		Here, as the response o/p is not a valid JSON giving error like this:
		Error:
			Parse error on line 1:
			...producer_block_id": None, "receipt": {"s
			-----------------------^
			Expecting 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '[', got 'undefined'

		So, capture txn_id by char no. i.e. {"transaction_id": "14e310c6e296560202ec808139d7e1b06901616f35b5c4a36ee0a4f065ec72a6"
	'''
	elapsed_time = time.time() - t_start
	elapsed_time = '{:.2f}'.format(elapsed_time)

	bot.send_message(message.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= 'MARKDOWN') if chain_type== "eos-mainnet" else bot.send_message(message.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= 'MARKDOWN')          # print the txn_id for successful transaction

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

		if r.hexists(str(message.chat.id), 'kycdocf') == True:
			# check if the value is not empty (in bytes)
			if r.hget(str(message.chat.id), 'kycdocf') != b'':
				img_data = r.hget(str(message.chat.id), 'kycdocf')			# get the 'base64' encoded image data
				with open(f"img_showf_{message.chat.id}.jpg", "wb") as fh:
					# decode the image as 'base64' encoding type & then write
					fh.write(base64.b64decode(img_data))			
				
				with open(f"img_showf_{message.chat.id}.jpg", 'rb') as photo:
					bot.send_photo(message.chat.id, photo, caption="Document front photo")
				
				os.remove(f"img_showf_{message.chat.id}.jpg")		# delete the file after use
		else:
			bot.send_message(message.chat.id, "Sorry! No <u>Document front</u> photo available.", parse_mode='HTML')

		if r.hexists(str(message.chat.id), 'kycdocb') == True:
			# check if the value is not empty (in bytes)
			if r.hget(str(message.chat.id), 'kycdocb') != b'':
				img_data = r.hget(str(message.chat.id), 'kycdocb')			# get the 'base64' encoded image data
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
		bot.send_message(message.chat.id, 'To view the KYC data on Blockchain DB, click [here](' + kyc_table_info_url.format(chain_name= chain_name, chat_id=message.chat.id) + ')', parse_mode='MARKDOWN')
	
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
	bot.send_message(call.message.chat.id, "Please, send your name. E.g.")
	bot.send_message(call.message.chat.id, "kycname Peter Bennett")


# -----------------------------callback: kyc_address------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_address')
def kyc_address_callback(call):
	bot.send_message(call.message.chat.id, "Please, send your address. E.g.")
	bot.send_message(call.message.chat.id, "kycaddr 1504 Liberty St.\nNew York, NY\n10004 USA")


@bot.message_handler(content_types=['text'])
def handle_text(message):
	if message.text.__contains__("kycname") or message.text.__contains__("kycaddr"):
		name = address = ''
		try:				# for Blockchain
			# push txn
			bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')

			if message.text.__contains__("kycname"):
				# "kycname Ramesh Kumar" --> "Ramesh Kumar"  Don't forget to strip whitespaces from front & back
				name = message.text.replace("kycname", "").strip()
				# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, name, "", "", "", "", message))
				asyncio.run(addmodkyc(message.chat.id, name, "", "", "", "", message))

			elif message.text.__contains__("kycaddr"):
				address = message.text.replace("kycaddr", "").strip()

				# convert address to it's hash to validate via Blockchain
				h = SHA256.new()
				h.update(bytes(address, 'utf-8'))
				address_hash = h.hexdigest()

				# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", address_hash, "", "", "", message))
				asyncio.run(addmodkyc(message.chat.id, "", address_hash, "", "", "", message))

			
			try:			# for Redis DB
				t_start = time.time()

				bot.send_message(message.chat.id, 'Saving name to Redis DB...')

				if message.text.__contains__("kycname"):
					r.hset(str(message.chat.id), 'name', name)
				elif message.text.__contains__("kycaddr"):
					r.hset(str(message.chat.id), 'address', address)

				elapsed_time = time.time() - t_start
				elapsed_time = '{:.2f}'.format(elapsed_time)

				bot.reply_to(message, f'Field saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.send_message(message.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except redis.exceptions.ConnectionError as e:
				bot.send_message(message.chat.id, f'Redis Database Connection Error')
		
		except EosRpcException as e:
			e = str(e).replace("\'", "\"")
			code_idx = e.find('code')
			code_val = int(e[code_idx+7:(code_idx+14)])
			# print(code_idx)
			# print(code_val)
			# print(type(code_val))
			if code_idx != -1:			# found "code" key
				if code_val == 3010001:						# Case-1: invalid name
					bot.send_message(message.chat.id, "Sorry! Your EOSIO account name doesn\'t exist on this chain.")
				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
					bot.send_message(message.chat.id, "Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity or symbol on this chain.")
				elif code_val == 3080004:
					bot.send_message(message.chat.id, f"Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
				else:
					bot.send_message(message.chat.id, f"Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
			else:						# NOT found "code" key
				bot.send_message(message.chat.id, f"Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")


			# chat.send(f"Assertion Error msg --> {json.loads(str(e))['what']}")          # print the message
			# chat.send(f"Assertion Error msg -->{str(e)}")          # print the message
		except EosAccountDoesntExistException:
			bot.send_message(message.chat.id, f'Your EOSIO account doesn\'t exist on this chain.')
		except EosAssertMessageException as e:
			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
			bot.send_message(message.chat.id, f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
		except EosDeadlineException:
			bot.send_message(message.chat.id, f'Transaction timed out. Please try again.')
		except EosRamUsageExceededException:
			bot.send_message(message.chat.id, f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
		except EosTxCpuUsageExceededException:
			bot.send_message(message.chat.id, f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
		except EosTxNetUsageExceededException:
			bot.send_message(message.chat.id, f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	else:
		bot.reply_to(message, "Not sure, what do you mean. \nPlease follow up with /help command.")

# @bot.message_handler(content_types=['text'])
# def save_kyc_address(message):
# 	bot.send_message(message.chat.id, "hello")
# 	if message.text.__contains__("kycaddr"):
# 		bot.send_message(message.chat.id, "found")
# 		# "kycaddr Ramesh Kumar" --> "Ramesh Kumar"  Don't forget to strip whitespaces from front & back
# 		address = message.text.replace("kycaddr", "").strip()

# 		# convert address to it's hash to validate via Blockchain
# 		h = SHA256.new()
# 		h.update(bytes(address, 'utf-8'))
# 		address_hash = h.hexdigest()
	
# 		try:				# for Blockchain
# 			# push txn
# 			bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')
# 			# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", address_hash, "", "", "", message))
# 			asyncio.run(addmodkyc(message.chat.id, "", address_hash, "", "", "", message))
			
# 			try:			# for Redis DB
# 				t_start = time.time()

# 				bot.send_message(message.chat.id, 'Saving address to Redis DB...')

# 				r.hset(str(message.chat.id), 'address', address)

# 				elapsed_time = time.time() - t_start
# 				elapsed_time = '{:.2f}'.format(elapsed_time)

# 				bot.reply_to(message, f'{address} \nsaved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
# 				bot.send_message(message.chat.id, 'To view your updated KYC, use /showkycinfo command.')

# 			except redis.exceptions.ConnectionError as e:
# 				bot.send_message(message.chat.id, f'Redis Database Connection Error')

# 		except EosRpcException as e:
# 			e = str(e).replace("\'", "\"")
# 			code_idx = e.find('code')
# 			code_val = int(e[code_idx+7:(code_idx+14)])
# 			# print(code_idx)
# 			# print(code_val)
# 			# print(type(code_val))
# 			if code_idx != -1:			# found "code" key
# 				if code_val == 3010001:						# Case-1: invalid name
# 					bot.send_message(message.chat.id, "Sorry! Your EOSIO account name doesn\'t exist on this chain.")
# 				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
# 					bot.send_message(message.chat.id, "Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity or symbol on this chain.")
# 				elif code_val == 3080004:
# 					bot.send_message(message.chat.id, f"Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
# 				else:
# 					bot.send_message(message.chat.id, f"Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
# 			else:						# NOT found "code" key
# 				bot.send_message(message.chat.id, f"Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")


# 			# chat.send(f"Assertion Error msg --> {json.loads(str(e))['what']}")          # print the message
# 			# chat.send(f"Assertion Error msg -->{str(e)}")          # print the message
# 		except EosAccountDoesntExistException:
# 			bot.send_message(message.chat.id, f'Your EOSIO account doesn\'t exist on this chain.')
# 		except EosAssertMessageException as e:
# 			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
# 			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
# 			bot.send_message(message.chat.id, f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
# 		except EosDeadlineException:
# 			bot.send_message(message.chat.id, f'Transaction timed out. Please try again.')
# 		except EosRamUsageExceededException:
# 			bot.send_message(message.chat.id, f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
# 		except EosTxCpuUsageExceededException:
# 			bot.send_message(message.chat.id, f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
# 		except EosTxNetUsageExceededException:
# 			bot.send_message(message.chat.id, f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	
# ---------------------------callback: kyc_docfrontimg------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_docfrontimg')
def kyc_docfrontimg_callback(call):
	bot.send_message(call.message.chat.id, "Please, send your document front image. E.g.")
	bot.send_photo(call.message.chat.id, open("../others/res/id_front.png", "rb"), caption="kycdocf")

# ---------------------------callback: kyc_docbackimg------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_docbackimg')
def kyc_docbackimg_callback(call):
	bot.send_message(call.message.chat.id, "Please, send your document back image. E.g.")
	bot.send_photo(call.message.chat.id, open("../others/res/id_back.png", "rb"), caption="kycdocb")


# ---------------------------callback: kyc_selfie------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_selfie')
def kyc_selfie_callback(call):
	bot.send_message(call.message.chat.id, "Please, send your selfie. E.g.")
	bot.send_photo(call.message.chat.id, open("../others/res/selfie.jpg", "rb"), caption="selfie")

# ---------------------------Handle photos: kycdocf, kycdocb, selfie---------------------------------------------
# receive photo with specific captions - kycdocf, kycdocb, selfie
@bot.message_handler(content_types=['photo'])
def receive_photo(message):
	if message.caption == "kycdocf" or message.caption == "kycdocb" or message.caption == "selfie":
		photo_fileid = message.photo[-1].file_id
		# bot.reply_to(message, f"photo msg detected. & the file_id is \n{photo_fileid}")
		# bot.send_photo(message.chat.id, f"{photo_fileid}")

		# get file info & file path
		file_info = bot.get_file(photo_fileid)

		# download from the Telegram server by 
		downloaded_file = bot.download_file(file_info.file_path)

		# with open("new_file.jpg", 'wb') as new_file:				# compressed file, Otherwise use 'png' format
		# Unique file created for each user & delete after use. Otherwise, there will be clash.
		with open(f"img_{message.caption}_{message.chat.id}.jpg", 'wb') as new_file:				
			new_file.write(downloaded_file)

		# send the photo which is downloaded first & then saved
		# bot.send_photo(message.chat.id, open(f"img_{message.caption}_{message.chat.id}.jpg", "rb"))				

		# encode the image as 'base64' encoding type
		img_encoded = base64.b64encode(open(f"img_{message.caption}_{message.chat.id}.jpg", "rb").read())

		# convert address to it's hash to validate via Blockchain
		h = SHA256.new()
		h.update(img_encoded)
		photo_hash = h.hexdigest()
	
		try:				# for Blockchain
			# push txn
			bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')
			if message.caption == "kycdocf":
				# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", "", photo_hash, "", "", message))
				asyncio.run(addmodkyc(message.chat.id, "", "", photo_hash, "", "", message))
			elif message.caption == "kycdocb":
				# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", "", "", photo_hash, "", message))
				asyncio.run(addmodkyc(message.chat.id, "", "", "", photo_hash, "", message))
			elif message.caption == "selfie":
				# asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", "", "", "", photo_hash, message))
				asyncio.run(addmodkyc(message.chat.id, "", "", "", "", photo_hash, message))

			try:			# for Redis DB
				t_start = time.time()

				bot.send_message(message.chat.id, 'Saving photo to Redis DB...')

				r.hset(str(message.chat.id), f"{message.caption}", img_encoded)
				elapsed_time = time.time() - t_start
				elapsed_time = '{:.2f}'.format(elapsed_time)

				bot.reply_to(message, f'Photo saved. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
				bot.send_message(message.chat.id, 'To view your updated KYC, use /showkycinfo command.')

			except (redis.exceptions.ConnectionError):
				bot.send_message(message.chat.id, f'Redis Database Connection Error')

			os.remove(f"img_{message.caption}_{message.chat.id}.jpg")		# delete the file after use

		except EosRpcException as e:
			e = str(e).replace("\'", "\"")
			code_idx = e.find('code')
			code_val = int(e[code_idx+7:(code_idx+14)])
			# print(code_idx)
			# print(code_val)
			# print(type(code_val))
			if code_idx != -1:			# found "code" key
				if code_val == 3010001:						# Case-1: invalid name
					bot.send_message(message.chat.id, "Sorry! Your EOSIO account name doesn\'t exist on this chain.")
				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
					bot.send_message(message.chat.id, "Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity or symbol on this chain.")
				elif code_val == 3080004:
					bot.send_message(message.chat.id, f"Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
				else:
					bot.send_message(message.chat.id, f"Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
			else:						# NOT found "code" key
				bot.send_message(message.chat.id, f"Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")


			# chat.send(f"Assertion Error msg --> {json.loads(str(e))['what']}")          # print the message
			# chat.send(f"Assertion Error msg -->{str(e)}")          # print the message
		except EosAccountDoesntExistException:
			bot.send_message(message.chat.id, f'Your EOSIO account doesn\'t exist on this chain.')
		except EosAssertMessageException as e:
			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
			bot.send_message(message.chat.id, f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
		except EosDeadlineException:
			bot.send_message(message.chat.id, f'Transaction timed out. Please try again.')
		except EosRamUsageExceededException:
			bot.send_message(message.chat.id, f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
		except EosTxCpuUsageExceededException:
			bot.send_message(message.chat.id, f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
		except EosTxNetUsageExceededException:
			bot.send_message(message.chat.id, f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	else:
		bot.reply_to(message, "Caption is not provided alongwith. So, please send photo again with an acceptable caption: \nkycdocf, kycdocb, selfie")




# ===========================command: /delkyc===========================
@bot.message_handler(commands=['delkyc'])
def delkyc_command(message):
	"""
		Delete user's KYC info from this bot via Blockchain
	"""
	try:				# for Blockchain
		# push txn
		bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')
		asyncio.get_event_loop().run_until_complete(delkyc(message.chat.id, message))
		
		try:			# for Redis DB
			t_start = time.time()

			bot.send_message(message.chat.id, 'Deleting KYC from Redis DB...')

			r.delete(str(message.chat.id))

			elapsed_time = time.time() - t_start
			elapsed_time = '{:.2f}'.format(elapsed_time)

			bot.send_message(message.chat.id, f'Your KYC is deleted. To add, use /addmodkyc command. \n\n*Response time: {elapsed_time} secs*', parse_mode='MARKDOWN')
			bot.send_message(message.chat.id, 'To view your updated KYC, use /showkycinfo command.')

		except redis.exceptions.ConnectionError as e:
			bot.send_message(message.chat.id, f'Redis Database Connection Error')

	except EosRpcException as e:
		e = str(e).replace("\'", "\"")
		code_idx = e.find('code')
		code_val = int(e[code_idx+7:(code_idx+14)])
		# print(code_idx)
		# print(code_val)
		# print(type(code_val))
		if code_idx != -1:			# found "code" key
			if code_val == 3010001:						# Case-1: invalid name
				bot.send_message(message.chat.id, "Sorry! Your EOSIO account name doesn\'t exist on this chain.")
			elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
				bot.send_message(message.chat.id, "Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity or symbol on this chain.")
			elif code_val == 3080004:
				bot.send_message(message.chat.id, f"Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
			else:
				bot.send_message(message.chat.id, f"Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
		else:						# NOT found "code" key
			bot.send_message(message.chat.id, f"Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")


		# chat.send(f"Assertion Error msg --> {json.loads(str(e))['what']}")          # print the message
		# chat.send(f"Assertion Error msg -->{str(e)}")          # print the message
	except EosAccountDoesntExistException:
		bot.send_message(message.chat.id, f'Your EOSIO account doesn\'t exist on this chain.')
	except EosAssertMessageException as e:
		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
		bot.send_message(message.chat.id, f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	except EosDeadlineException:
		bot.send_message(message.chat.id, f'Transaction timed out. Please try again.')
	except EosRamUsageExceededException:
		bot.send_message(message.chat.id, f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
	except EosTxCpuUsageExceededException:
		bot.send_message(message.chat.id, f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
	except EosTxNetUsageExceededException:
		bot.send_message(message.chat.id, f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');

# ================================================MAIN===========================================================================
# bot.polling(none_stop= True)			# for Production
bot.polling()							# for DEBUG