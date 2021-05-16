import botogram
# import redis
import json
import asyncio

from aioeos import EosAccount, EosJsonRpc, EosTransaction
from aioeos import types

from aioeos.exceptions import EosAccountDoesntExistException
from aioeos.exceptions import EosAssertMessageException
from aioeos.exceptions import EosDeadlineException
from aioeos.exceptions import EosRamUsageExceededException
from aioeos.exceptions import EosTxCpuUsageExceededException
from aioeos.exceptions import EosTxNetUsageExceededException

from input import *

# -------------------------------------------------------About Bot--------------------------------------------------------------------
bot = botogram.create(API_key)
bot.about = "This is a Tip Bot."
bot.owner = "@abhi3700"

# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
# r = redis.from_url(REDIS_URL)

# ===================================================func for addmodkyc ACTION========================================================
async def addmodkyc(
		from_id,
		from_username,
		to_ac,
		quantity,
		memo,
		chat
	):
	contract_account = EosAccount(
	  name=tip_eosio_ac,
	  private_key=tip_ac_private_key
	)

	action = types.EosAction(
		account=tip_eosio_ac,
		name=withdraw_action,
		authorization=[contract_account.authorization(tip_ac_key_perm)],
		data={
			'from_id': from_id,
			'from_username': from_username,
			'to_ac': to_ac,
			'quantity': quantity,
			'memo': memo
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
	chat.send(f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]}") if chain_type== "eos-mainnet" else chat.send(f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]}")          # print the txn_id for successful transaction

# ===================================================func for delkyc ACTION===================================================================



# ===================================================command: /addkyc===========================================================================
@bot.command("addkyc")
def addkyc_command(chat, message, args):
	"""
		Add KYC to this bot via Blockchain
		Demo:
		=====
		User: 
			/addkyc tipuser11111 1.0000 EOS
		Bot:
			DONE!
	"""
	# if len(args) == 3:
	# 	# chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}")        # for testing
	# 	try:
	# 		# push txn
	# 		asyncio.get_event_loop().run_until_complete(withdraw(chat.id, message.sender.username, args[0], args[1] + " " + args[2], "", chat))

	# 	except EosAccountDoesntExistException:
	# 		chat.send(f'Your EOSIO account doesn\'t exist on this chain.')
	# 	except EosAssertMessageException as e:
	# 		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
	# 		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
	# 		chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	# 	except EosDeadlineException:
	# 		chat.send(f'Transaction timed out. Please try again.')
	# 	except EosRamUsageExceededException:
	# 		chat.send(f'Transaction requires more RAM than what’s available on the account. Please contact the Bot owner {bot.owner}.');
	# 	except EosTxCpuUsageExceededException:
	# 		chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
	# 	except EosTxNetUsageExceededException:
	# 		chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');

	# else:
	# 	chat.send("Please enter withdrawal request in this format: /withdrawmemo ACCOUNT AMOUNT SYMBOL \n(e.g. /withdraw tipuser11111 1.0000 EOS)")

	btns = botogram.Buttons()

	btns[0].callback("Name", "kyc_name")     						# button - Name
	btns[0].callback("Address", "kyc_address")     					# button - Address
	btns[1].callback("Document front image", "kyc_docfrontimg")     # button - Document front photo
	btns[2].callback("Document back image", "kyc_docbackimg")     	# button - Document back photo
	btns[3].callback("Selfie image", "kyc_selfie") 					   	# button - Selfie

	chat.send("Please, select one option to add KYC", attach= btns)

# ---------------------------------------------------callback: kyc_name------------------------------------------------------------------------------
@bot.callback("kyc_name")
def kyc_name_callback(query, chat, message):
    chat.send("Please, send your name. E.g.")
    chat.send("kycname Peter Bennett")

@bot.message_contains("kycname")
def save_kycname(chat, message):
	name = message.text.replace("kycname", "")
	message.reply(f'{name} \nsaved.')

# ---------------------------------------------------callback: kyc_address------------------------------------------------------------------------------
@bot.callback("kyc_address")
def kyc_address_callback(query, chat, message):
    chat.send("Please, send your address. E.g.")
    chat.send("kycaddr 1504 Liberty St.\nNew York, NY\n10004 USA")

@bot.message_contains("kycaddr")
def save_kycaddress(chat, message):
	address = message.text.replace("kycaddr", "")
	message.reply(f'{address} \nsaved.')

# ---------------------------------------------------callback: kyc_docfrontimg------------------------------------------------------------------------------
@bot.callback("kyc_docfrontimg")
def kyc_docfrontimg_callback(query, chat, message):
    chat.send("Please, send your document address. E.g.")
    chat.send("kycaddr 1504 Liberty St.\nNew York, NY\n10004 USA")

@bot.message_contains("kycdocf")
def save_kycaddress(chat, message):
	address = message.text.replace("kycaddr", "")
	message.reply(f'{address} \nsaved.')


# Backup plan
'''
/addkycname Abhijit Chandra Roy
args[0] to args[-1]

/add
'''

# ================================================MAIN===========================================================================
if __name__ == "__main__":
	bot.run()