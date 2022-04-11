# kyc_bot
* [DEPRECATED] A WhatsApp Bot which allows a user to fill KYC on Blockchain
* A Telegram Bot which allows a user to fill KYC on Blockchain

## Features
* [x] add kyc info
	- here, `/addkyc` is to show the option like this:
```
| name | address | doc ID front photo |
| doc ID back photo | selfie photo |
```
* [x] modify kyc info
	- here, `/editkyc` is to edit any fields of KYC
```
| name | address | doc ID front photo |
| doc ID back photo | selfie photo |
```
* [x] delete kyc
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
* [x] Get IPFS URL after successful photo upload [NOT RECOMMENDED as IPFS is public now]
* [ ] Bot Get User photo after upload in Telegram
* [x] redis cloud setup
* [x] contracts interaction with the bot

## Product
### Demo
* Telegram Bot
	- Here, individual account on blockchain is not created, so, all the transaction history is available with the contract's history [here](https://jungle3.bloks.io/account/kycteosiobot)
	- Currently, all the data except name are hashed. The privacy in EOSIO Blockchains is [coming soon](https://eos.io/news/blockchain-privacy/)
	- Here, there is no user key management is needed. Just one caution: to keep the telegram account safe.
	- [NOT RECOMMENDED as IPFS is public now] the image url is stored on IPFS (currently public, private). Unlike Cloud services, IPFS is content-based (content-addressed) and not location-based (location-addressed) like http protocol. For more, read [this](https://medium.com/0xcode/using-ipfs-for-distributed-file-storage-systems-61226e07a6f)

> When a storage system is based on location, it is about identifying a server by its host name using a DNS server. This tracks a host by a logical addressing scheme (e.g. IP address) mapped to a user friendly name. If the host changes its name or address, it must also be modified in the name service table.

> Content-based addressing storage pertains to the content to get data from the network. This requires a content identifier that determines the physical location of a file. In this case the data is accessed based on its cryptographic hash rather than logical address, much like a digital fingerprint of a file. The network will always return the same content based on that hash regardless of who uploaded the file, where and when it was uploaded.

* App - Android, iOS, & ipfs cloud privacy is also evolving.
	- Here, individual account on blockchain is created & hence it has all the transaction history. E.g. [here](https://jungle3.bloks.io/account/kycusr111111)
	- wallets is integrated into the DApp.

## References
