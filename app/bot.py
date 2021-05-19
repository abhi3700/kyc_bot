import botogram
import redis
import json
import asyncio
import time
from Crypto.Hash import SHA256

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
bot = botogram.create(API_key)
bot.about = "This is a KYC Bot."
bot.owner = "@abhi3700"

# --------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL, ssl_cert_reqs=None)		# ssl_verify to false
# =========================func for IPFS cloud========================================================
def getipfsurl(img_path, chat):
	headers = {
		'accept': 'application/json',
		'Content-Type': 'image/png',
		'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGU0QTRhOTNGQzBlZTI4MjEyMjBiQTI0RTgwNTkxNjg2NzY1QUFCNDMiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTYyMTAyMjY0NDQ1OCwibmFtZSI6Imt5Y2JvdCJ9.rkAqB60ANzkwoe5XGIP89fTrxxiyK4zkIRq6bc5NQ7c',
	}

	r = requests.post(
		url = API_ENDPOINT, 
		headers= headers, 
		data= open(img_path, 'rb').read()			# e.g. img_path = '../img/nft_market.jpg'
		)

	# url = ''
	if (r.status_code == 200):
		cid = r.json()['value']['cid']
		# print(cid)			# print IPFS CID
		chat.send(f'Get the image at this url: https://{cid}.ipfs.dweb.link/')		# print the img url
	else:
		chat.send(f'Some problem occurred during uploading: {r.status_code}')


# =========================func for addmodkyc ACTION========================================================
async def addmodkyc(
		plat_user_id,
		fullname,
		address_hash,
		document_id_front_hash,
		document_id_back_hash,
		selfie_hash,
		chat
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

	chat.send(f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]}") if chain_type== "eos-mainnet" else chat.send(f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", syntax='markdown')          # print the txn_id for successful transaction

# =======================func for delkyc ACTION===================================================================
async def delkyc(
		plat_user_id,
		chat
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

	chat.send(f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]}") if chain_type== "eos-mainnet" else chat.send(f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]} \n\n*Response time: {elapsed_time} secs*", syntax='markdown')          # print the txn_id for successful transaction

# ===========================command: /showkycinfo===========================================================================
@bot.command("showkycinfo")
def showkycinfo_command(chat, message, args):
	'''
		Show user's updated KYC info 
	'''
	name = address = doc_frontf_url = doc_backf_url = selfie_url = ''		# initialize all at a time
	try:
		chat.send('Please wait...')
		t_start = time.time()
		if r.hexists(str(chat.id), 'name') == True:
			name = r.hget(str(chat.id), 'name').decode('utf-8')		
		if r.hexists(str(chat.id), 'address') == True:
			address = r.hget(str(chat.id), 'address').decode('utf-8')
		if r.hexists(str(chat.id), 'document_photo_front_url') == True:
			doc_frontf_url = r.hget(str(chat.id), 'document_photo_front_url').decode('utf-8')
		if r.hexists(str(chat.id), 'document_photo_back_url') == True:
			doc_backf_url = r.hget(str(chat.id), 'document_photo_back_url').decode('utf-8')
		if r.hexists(str(chat.id), 'selfie_photo_url') == True:
			selfie_url = r.hget(str(chat.id), 'selfie_photo_url').decode('utf-8')
		
		elapsed_time = time.time() - t_start
		elapsed_time = '{:.2f}'.format(elapsed_time)

		chat.send(f'<u>Your updated KYC info is shown here</u>: \n\n - Name: {name} \n - Address: {address} \n - Document Front Photo URL: {doc_frontf_url} \n - Document Back Photo URL: {doc_backf_url} \n - Selfie Photo URL: {selfie_url} \n\n<b>Response time: {elapsed_time} secs</b>', syntax='html')
		chat.send('To view the KYC data on Blockchain DB, click [here](' + kyc_table_info_url.format(chain_name= chain_name, chat_id=chat.id) + ')', syntax='markdown')
	
	except redis.exceptions.ConnectionError as e:
		chat.send(f'Redis Database Connection Error')
	
# ===========================command: /upimgipfs===========================================================================
@bot.command("getipfsurl")
def getipfsurl_command(chat, message, args):
	pass

# ===========================command: /addmodkyc===========================================================================
@bot.command("addmodkyc")
def addmodkyc_command(chat, message, args):
	"""
		Add/Modify KYC to this bot via Blockchain
	"""
	btns = botogram.Buttons()

	btns[0].callback("Name", "kyc_name")     						# button - Name
	btns[0].callback("Address", "kyc_address")     					# button - Address
	btns[1].callback("Document front image", "kyc_docfrontimg")     # button - Document front photo
	btns[2].callback("Document back image", "kyc_docbackimg")     	# button - Document back photo
	btns[3].callback("Selfie image", "kyc_selfie") 					# button - Selfie

	chat.send("Please, select one option to add KYC", attach= btns)

# --------------------------------callback: kyc_name------------------------------------------------------------------------------
@bot.callback("kyc_name")
def kyc_name_callback(query, chat, message):
	chat.send("Please, send your name. E.g.")
	chat.send("kycname Peter Bennett")

@bot.message_contains("kycname")
def save_kyc_name(chat, message):
	name = message.text.replace("kycname", "")
	try:				# for Blockchain
		# push txn
		chat.send('Validating on EOS Blockchain...')
		asyncio.get_event_loop().run_until_complete(addmodkyc(chat.id, name, "", "", "", "", chat))
		
		try:			# for Redis DB
			t_start = time.time()

			chat.send('Saving name to Redis DB...')

			r.hset(str(chat.id), 'name', name)

			elapsed_time = time.time() - t_start
			elapsed_time = '{:.2f}'.format(elapsed_time)

			message.reply(f'{name} \nsaved. \n\n*Response time: {elapsed_time} secs*')
			chat.send('To view your updated KYC, use /showkycinfo command.')

		except redis.exceptions.ConnectionError as e:
			chat.send(f'Redis Database Connection Error')

	except EosAccountDoesntExistException:
		chat.send(f'Your EOSIO account doesn\'t exist on this chain.')
	except EosAssertMessageException as e:
		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
		chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	except EosDeadlineException:
		chat.send(f'Transaction timed out. Please try again.')
	except EosRamUsageExceededException:
		chat.send(f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
	except EosTxCpuUsageExceededException:
		chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
	except EosTxNetUsageExceededException:
		chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');


# -----------------------------callback: kyc_address------------------------------------------------------------------------------
@bot.callback("kyc_address")
def kyc_address_callback(query, chat, message):
	chat.send("Please, send your address. E.g.")
	chat.send("kycaddr 1504 Liberty St.\nNew York, NY\n10004 USA")

@bot.message_contains("kycaddr")
def save_kyc_address(chat, message):
	address = message.text.replace("kycaddr", "")
	h = SHA256.new()
	h.update(bytes(address, 'utf-8'))
	address_hash = h.hexdigest()
	
	try:				# for Blockchain
		# push txn
		chat.send('Validating on EOS Blockchain...')
		asyncio.get_event_loop().run_until_complete(addmodkyc(chat.id, "", address_hash, "", "", "", chat))
		
		try:			# for Redis DB
			t_start = time.time()

			chat.send('Saving address to Redis DB...')

			r.hset(str(chat.id), 'address', address)

			elapsed_time = time.time() - t_start
			elapsed_time = '{:.2f}'.format(elapsed_time)

			message.reply(f'{address} \nsaved. \n\n*Response time: {elapsed_time} secs*')
			chat.send('To view your updated KYC, use /showkycinfo command.')

		except redis.exceptions.ConnectionError as e:
			chat.send(f'Redis Database Connection Error')

	except EosAccountDoesntExistException:
		chat.send(f'Your EOSIO account doesn\'t exist on this chain.')
	except EosAssertMessageException as e:
		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
		chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	except EosDeadlineException:
		chat.send(f'Transaction timed out. Please try again.')
	except EosRamUsageExceededException:
		chat.send(f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
	except EosTxCpuUsageExceededException:
		chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
	except EosTxNetUsageExceededException:
		chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	
# ---------------------------callback: kyc_docfrontimg------------------------------------------------------------------------------
@bot.callback("kyc_docfrontimg")
def kyc_docfrontimg_callback(query, chat, message):
	chat.send("Please, send your document front image. E.g.")
	chat.send_photo(url="https://bafybeif7o6gbojzob7tjl3g74425nb54v5als6rx7e4ytadwrtq3vcpr7u.ipfs.dweb.link/",
					caption= "kycdocf"
					)
	# chat.send("To get IPFS url for any image uploaded to IPFS, use this command - /getipfsurl")

@bot.message_contains("kycdocf")
def save_kyc_docfrontimg(chat, message):
	# address = message.text.replace("kycdocf", "")

	message.reply(f"{message.caption}")
	message.reply(f"{message.id}, {message.sender.name}, {message.date}, {message.chat.id} + {message.chat.username}")
	photo_file = message.photo
	message.reply(f"{type(photo_file)}")
	# photo_file.download('kycdocf_photo.jpg')
	# message.reply(f"{message.photo[-1].get_file()}")

	# updates = bot.api.call("getUpdates", {"chat_id": chat.id, "user_id": message.sender.id})
	# updates = bot.api.call("getUpdates")
	# if updates["ok"] == True:
	# 	chat.send("OK")
	# 	chat.send(f'{type(updates)}')
	# 	txt_msgs = updates["result"].reverse()
	# 	chat.send(f"{len(txt_msgs)}")
	# 	txt_msg = txt_msgs[0]["message"]["text"]
	# 	chat.send(f"{type(txt_msgs)}")
	# 	chat.send(f"{txt_msg}")
	# 	message.reply(f'{message.id}')

	# else:
	# 	chat.send("Problem connecting to the Bot server.")

	# chat.send(f"{message.id}")
	# message.reply(f'{message.id}')
	# message.reply('{file_id} \nsaved.'.format(file_id=str(photo2.file_id)), reply_to = message.id)

# @bot.message_matches("kycdocf")
# def save_kyc_docfrontimg(chat, message):
# 	# address = message.text.replace("kycdocf", "")

# 	message.reply(f"{message.caption}")
# 	message.reply(f"{message.id}, {message.sender.name}, {message.date}, {message.chat.id} + {message.chat.username}")
# 	message.reply(f"{message.photo}")


# @bot.message_contains("kycdocf")
# def demo(chat, message):
#     status = bot.api.call("getMessages", {"chat_id": chat.id, "user_id": message.sender.id});

# 	if status == "OK":
# 	else:
# 		chat.send("Connection error.")	


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
@bot.command("delkyc")
def delkyc_command(chat, message, args):
	"""
		Delete user's KYC info from this bot via Blockchain
	"""
	try:				# for Blockchain
		# push txn
		chat.send('Validating on EOS Blockchain...')
		asyncio.get_event_loop().run_until_complete(delkyc(chat.id, chat))
		
		try:			# for Redis DB
			t_start = time.time()

			chat.send('Deleting KYC from Redis DB...')

			r.delete(str(chat.id))

			elapsed_time = time.time() - t_start
			elapsed_time = '{:.2f}'.format(elapsed_time)

			chat.send(f'Your KYC is deleted. To add, use /addmodkyc command. \n\n*Response time: {elapsed_time} secs*')
			chat.send('To view your updated KYC, use /showkycinfo command.')

		except redis.exceptions.ConnectionError as e:
			chat.send(f'Redis Database Connection Error')

	except EosAccountDoesntExistException:
		chat.send(f'Your EOSIO account doesn\'t exist on this chain.')
	except EosAssertMessageException as e:
		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
		chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	except EosDeadlineException:
		chat.send(f'Transaction timed out. Please try again.')
	except EosRamUsageExceededException:
		chat.send(f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
	except EosTxCpuUsageExceededException:
		chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
	except EosTxNetUsageExceededException:
		chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');

# ================================================MAIN===========================================================================
if __name__ == "__main__":
	bot.run()