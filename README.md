# kyc_bot
* [DEPRECATED] A WhatsApp Bot which allows a user to fill KYC on Blockchain
* A Telegram Bot which allows a user to fill KYC on Blockchain

## Features
* [ ] add kyc info
	- here, `/addkyc` is to show the option like this:
```
| name | address | doc ID front photo |
| doc ID back photo | selfie photo |
```
* [ ] modify kyc info
	- here, `/editkyc` is to edit any fields of KYC
```
| name | address | doc ID front photo |
| doc ID back photo | selfie photo |
```
* [ ] delete kyc
	- here, `/delkyc` is to delete kyc 

## Coding

## Database
* Cloud: Redis on Heroku
	- by default, the values are not set, if it is identical with the previously stored. 1 -> success
```
> hset 232532532 name abhijit
1
> hset 232532532 name abhijit
0
```

## Contracts
* [kycweosiobot](https://github.com/abhi3700/eosio_kyc_contracts)

## Modules
* [x] Get IPFS URL after successful photo upload
* [ ] Bot Get User photo after upload in Telegram
* [x] redis cloud setup
* [ ] contracts interaction with the bot

## Product
### Demo
* Telegram Bot
	- Here, individual account on blockchain is not created, so, all the transaction history is available with the contract's history [here](https://jungle3.bloks.io/account/kycteosiobot)
	- Currently, all the data except name are hashed. The privacy in EOSIO Blockchains is [coming soon](https://eos.io/news/blockchain-privacy/)
	- Here, there is no user key management is needed. Just one caution: to keep the telegram account safe.
* App - Android, iOS, & ipfs cloud privacy is also evolving.
	- Here, individual account on blockchain is created & hence it has all the transaction history. E.g. [here](https://jungle3.bloks.io/account/kycusr111111)
	- wallets is integrated into the DApp.

## References
