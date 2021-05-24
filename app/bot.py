import telebot
import redis
import json
import asyncio
import time
from Crypto.Hash import SHA256
# import requests

from aioeos import EosAccount, EosJsonRpc, EosTransaction
from aioeos import types

from aioeos.exceptions import EosAccountDoesntExistException
from aioeos.exceptions import EosAssertMessageException
from aioeos.exceptions import EosDeadlineException
from aioeos.exceptions import EosRamUsageExceededException
from aioeos.exceptions import EosTxCpuUsageExceededException
from aioeos.exceptions import EosTxNetUsageExceededException

from input import *

# --------------------About Bot--------------------------------------------------------------------
bot= telebot.TeleBot(token= API_key, parse_mode= None)			# You can set parse_mode by default. HTML or MARKDOWN
bot.about = "This is a KYC Bot."
bot.owner = "@abhi3700"

# --------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL, ssl_cert_reqs=None)		# ssl_verify to false


# ----------------------------------------------
gen_markup = types.ReplyKeyboardRemove(selective=False)


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

	bot.send_message(message.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= MARKDOWN) if chain_type== "eos-mainnet" else bot.send_message(message.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= MARKDOWN)          # print the txn_id for successful transaction

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

	bot.send_message(message.chat.id, f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= MARKDOWN) if chain_type== "eos-mainnet" else bot.send_message(message.chat.id, f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", parse_mode= MARKDOWN)          # print the txn_id for successful transaction

# ===========================command: /showkycinfo===========================================================================
@bot.message_handler(commands=['showkycinfo'])
def showkycinfo_command(message):
	'''
		Show user's updated KYC info 
	'''
	name = address = doc_frontf_url = doc_backf_url = selfie_url = ''		# initialize all at a time
	try:
		bot.send_message(message.chat.id, 'Please wait...')
		t_start = time.time()
		if r.hexists(str(message.chat.id), 'name') == True:
			name = r.hget(str(message.chat.id), 'name').decode('utf-8')		
		elif r.hexists(str(message.chat.id), 'address') == True:
			address = r.hget(str(message.chat.id), 'address').decode('utf-8')
		elif r.hexists(str(message.chat.id), 'document_photo_front_url') == True:
			doc_frontf_url = r.hget(str(message.chat.id), 'document_photo_front_url').decode('utf-8')
		elif r.hexists(str(message.chat.id), 'document_photo_back_url') == True:
			doc_backf_url = r.hget(str(message.chat.id), 'document_photo_back_url').decode('utf-8')
		elif r.hexists(str(message.chat.id), 'selfie_photo_url') == True:
			selfie_url = r.hget(str(message.chat.id), 'selfie_photo_url').decode('utf-8')
		
		elapsed_time = time.time() - t_start
		elapsed_time = '{:.2f}'.format(elapsed_time)

		bot.send_message(message.chat.id, f'<u>Your updated KYC info is shown here</u>: \n\n - Name: {name} \n - Address: {address} \n - Document Front Photo URL: {doc_frontf_url} \n - Document Back Photo URL: {doc_backf_url} \n - Selfie Photo URL: {selfie_url} \n\n<b>Response time: {elapsed_time} secs</b>', parse_mode=HTML)
		bot.send_message(message.chat.id, 'To view the KYC data on Blockchain DB, click [here](' + kyc_table_info_url.format(chain_name= chain_name, chat_id=message.chat.id) + ')', parse_mode=HTML)
	
	except redis.exceptions.ConnectionError as e:
		chat.send(f'Redis Database Connection Error')
	
# ===========================command: /addmodkyc===========================================================================
@bot.message_handler(commands=['addmodkyc'])
def addmodkyc_command(message):
	"""
		Add/Modify KYC to this bot via Blockchain
	"""
	markup = types.InlineKeyboardMarkup(row_width=2)   # 'one_time_keyboard' hides the keyboard automatically when just after pressing button
	
	itembtn1 = types.InlineKeyboardButton('Name', callback_data = "kyc_name")
	itembtn2 = types.InlineKeyboardButton('Address', callback_data= "kyc_address")
	itembtn3 = types.InlineKeyboardButton('Document front image', callback_data= "kyc_docfrontimg")
	itembtn4 = types.InlineKeyboardButton('Document back image', callback_data= "kyc_docbackimg")
	itembtn5 = types.InlineKeyboardButton('Selfie image', callback_data= "kyc_selfie")
	
	markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

	bot.send_message(message.chat.id, "Please, select one option to add KYC", reply_markup= markup)

# --------------------------------callback: kyc_name------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_name')
def kyc_name_callback(message):
	bot.send_message(message.chat.id, "Please, send your name. E.g.")
	bot.send_message(message.chat.id, "kycname Peter Bennett")

# @bot.message_contains("kycname")
@bot.message_handler(content_types=['text'])
def save_kyc_name(message):
	if message.text.__contains__("kycname"):
		# "kycname Ramesh Kumar" --> "Ramesh Kumar"  Don't forget to strip whitespaces from front & back
		name = message.text.replace("kycname", "").strip()
		try:				# for Blockchain
			# push txn
			bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')
			asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, name, "", "", "", "", message))
			
			try:			# for Redis DB
				t_start = time.time()

				bot.send_message(message.chat.id, 'Saving name to Redis DB...')

				r.hset(str(message.chat.id), 'name', name)

				elapsed_time = time.time() - t_start
				elapsed_time = '{:.2f}'.format(elapsed_time)

				bot.reply_to(message, f'{name} \nsaved. \n\n*Response time: {elapsed_time} secs*')
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


# -----------------------------callback: kyc_address------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'kyc_address')
def kyc_address_callback(message):
	chat.send("Please, send your address. E.g.")
	chat.send("kycaddr 1504 Liberty St.\nNew York, NY\n10004 USA")

# @bot.message_contains("kycaddr")
@bot.message_handler(content_types=['text'])
def save_kyc_address(message):
	if message.text.__contains__("kycname"):
		# "kycaddr Ramesh Kumar" --> "Ramesh Kumar"  Don't forget to strip whitespaces from front & back
		address = message.text.replace("kycaddr", "").strip()

		# convert address to it's hash to validate via Blockchain
		h = SHA256.new()
		h.update(bytes(address, 'utf-8'))
		address_hash = h.hexdigest()
	
		try:				# for Blockchain
			# push txn
			bot.send_message(message.chat.id, 'Validating on EOSIO Blockchain...')
			asyncio.get_event_loop().run_until_complete(addmodkyc(message.chat.id, "", address_hash, "", "", "", message))
			
			try:			# for Redis DB
				t_start = time.time()

				bot.send_message(message.chat.id, 'Saving address to Redis DB...')

				r.hset(str(message.chat.id), 'address', address)

				elapsed_time = time.time() - t_start
				elapsed_time = '{:.2f}'.format(elapsed_time)

				bot.reply_to(message, f'{address} \nsaved. \n\n*Response time: {elapsed_time} secs*')
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
	
# ---------------------------callback: kyc_docfrontimg------------------------------------------------------------------------------
@bot.callback("kyc_docfrontimg")
def kyc_docfrontimg_callback(query, chat, message):
	chat.send("Please, send your document front image. E.g.")
	chat.send_photo(url="https://bafybeif7o6gbojzob7tjl3g74425nb54v5als6rx7e4ytadwrtq3vcpr7u.ipfs.dweb.link/",
					caption= "kycdocf"
					)
	# chat.send("To get IPFS url for any image uploaded to IPFS, use this command - /getipfsurl")

# @bot.message_contains("kycdocf", multiple=True)
@bot.message_contains("kycdocf")
def save_kyc_docfrontimg(chat, message):
	# address = message.text.replace("kycdocf", "")

	message.reply(f"{message.caption}")
	message.reply(f"{message.id}, {message.sender.name}, {message.date}, {message.chat.id} + {message.chat.username}")
	photo_file = message.photo.serialize()
	message.reply(f"{type(photo_file)}")
	# doc_file = message.document
	# message.reply(f"{type(doc_file.file_id)}")

	# if message.photo:
	# 	message.download_media('test.jpg') # to download the image
	# 	img = message.media # to store the image to later usage
	# 	chat.send("photo is downloaded")
	# photo_file.download('kycdocf_photo.jpg')
	# message.reply(f"{message.photo[-1].get_file()}")

	# updates = bot.api.call("getUpdates", {"chat_id": chat.id, "user_id": message.sender.id})
	# updates = bot.api.call("getUpdates")

	# chat.send(f"{message.id}")
	# message.reply(f'{message.id}')
	# message.reply('{file_id} \nsaved.'.format(file_id=str(photo2.file_id)), reply_to = message.id)

# @bot.message_matches("kycdocf")
# def save_kyc_docfrontimg(chat, message):
# 	# address = message.text.replace("kycdocf", "")

# 	message.reply(f"{message.caption}")
# 	message.reply(f"{message.id}, {message.sender.name}, {message.date}, {message.chat.id} + {message.chat.username}")
# 	message.reply(f"{message.photo}")


# ---------------------------callback: kyc_docbackimg------------------------------------------------------------------------------
@bot.callback("kyc_docbackimg")
def kyc_docbackimg_callback(query, chat, message):
	chat.send("Please, send your document back image. E.g.")
	chat.send("kycdocb https://bafybeiaxtcggahcg5lnd5uhgvr2zjwwp5mttiy2nzhx23phzdylk6wbtdi.ipfs.dweb.link/")

@bot.message_contains("kycdocb")
def save_kyc_docbackimg(chat, message):
	# address = message.text.replace("kycdocb", "")
	photo = message.photo
	# save_path = 
	# photo.save()
	message.reply(f'{photo.file_id} \nsaved.')

# ---------------------------callback: kyc_selfie------------------------------------------------------------------------------
@bot.callback("kyc_selfie")
def kyc_selfie_callback(query, chat, message):
	chat.send("Please, send your selfie. E.g.")
	chat.send("kycselfie https://bafybeiepbvi4js4b6xvzzb2q3uss6rseqedcfvdzx5yvmnjgncfispb6me.ipfs.dweb.link/")

@bot.message_contains("kycselfie")
def save_kyc_selfieimg(chat, message):
	# address = message.text.replace("kycselfie", "")
	photo = message.photo
	# save_path = 
	# photo.save()
	message.reply(f'{photo.file_id} \nsaved.')


# Backup plan
'''
/addmodkycname Abhijit Chandra Roy
args[0] to args[-1]

/add
'''

# ===========================command: /delkyc===========================================================================
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

			bot.send_message(message.chat.id, f'Your KYC is deleted. To add, use /addmodkyc command. \n\n*Response time: {elapsed_time} secs*')
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
if __name__ == "__main__":
	bot.run()