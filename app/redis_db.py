"""
    This file - `db.py` is to check the database data.
"""

import redis
import datetime
import json
from input import REDIS_URL


# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

# ----------------------------------------------------------------
# phoneno = "8143243443"
# username = "abhi3700"
# country = "India"

# product_a = dict(username= username, country= country, key_count= 3, datetime= str(datetime.date.today()))
# r.hset(phoneno, "ProductA", json.dumps(product_a))

# product_b = dict(username= username, country= country, key_count= 5, datetime= str(datetime.date.today()))
# r.hset(phoneno, "ProductB", json.dumps(product_b))

# print(r.hget(phoneno, "ProductA").decode('utf-8'))
# print(r.hget(phoneno, "ProductB").decode('utf-8'))


# # count the key
# newkey = json.loads(r.hget(phoneno, "ProductA").decode('utf-8')).get("key_count") + 1
# print(newkey)

# # json.loads() converts from string to dictionary. This is to access the get() function
# print(json.loads(r.hget(phoneno, "ProductA").decode('utf-8')).get("username"))
# print(json.dumps(r.get(phoneno), indent= 2))
# r.delete('DUMMY')
# print(r.keys())

# for key in r.keys():
#     # print(key.decode('utf-8'))
#     print(json.loads(r.hget(key.decode('utf-8'), "ProductA").decode('utf-8')).get('username'))
#     print(json.loads(r.hget(key.decode('utf-8'), "ProductA").decode('utf-8')).get('country'))
#     print(json.loads(r.hget(key.decode('utf-8'), "ProductA").decode('utf-8')).get('key'))
#     print(json.loads(r.hget(key.decode('utf-8'), "ProductA").decode('utf-8')).get('datetime'))
#     # print(json.loads(r.hget(phone_global, "ProductA").decode('utf-8')).get("country"))

# print(r.keys())

# phoneno1 = '+918146734455'
# uname1 = 'abhi3701'

# phoneno2 = '+918147424326734455'
# uname2 = 'abhi3702'

# phoneno3 = '+91565461474243267344'
# uname3 = 'abhi3703'

# r.hset(phoneno1, "product_a", json.dumps(dict(username= uname1)))
# r.hset(phoneno2, "product_a", json.dumps(dict(username= uname2)))
# r.hset(phoneno3, "product_a", json.dumps(dict(username= uname3)))

# print(json.loads(r.hget(phoneno1, "product_a").decode('utf-8')).get('username'))
# OR
# print(json.loads(r.hget(phoneno1, "product_a").decode('utf-8'))['username'])
# print(type(json.loads(r.hget(phoneno, "product_a").decode('utf-8'))))     # dict

# dict_nested2_val2 = json.loads(r.hget(phoneno, "product_a").decode('utf-8'))
# key_nested2 = ""

# try:
#     key_nested2 = list(dict_nested2_val2.keys())[list(dict_nested2_val2.values()).index('abhi3701')]       # get the key corresponding to value - 'India'
# except ValueError:      # ignore this exception error when item not found
#     pass
# print(key_nested2)


# phoneno2 = '+913257864235'
# r.hset(phoneno2, "username", uname)
# key_phone = ""
# for k in r.keys():
#     # print(k.decode('utf-8'))
#     dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "product_a"))
#     if dict_nested2_val2['username'] == 'abhi3700':
#         key_phone = k.decode('utf-8')
# print(key_phone)
# if key_phone == "":
#     print("Username doesn't exist")
    # try:
    #     key_nested2 = list(dict_nested2_val2.keys())[list(dict_nested2_val2.values()).index('abhi3701')]       # get the key corresponding to value - 'India'
    # except ValueError:      # ignore this exception error when item not found
    #     pass

print(r.keys())

# delete all stored keys
# for k in r.keys():
#     r.delete(k)

for k in r.keys():
    k_decoded = k.decode('utf-8')
    # print(json.loads(r.hget(k_decoded, "product_a").decode('utf-8')))
    print(json.loads(r.hget(k_decoded, "info").decode('utf-8')))
