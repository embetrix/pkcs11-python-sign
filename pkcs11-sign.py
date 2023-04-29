#! /usr/bin/env python3
#
# works only with NitroKey
# export PKCS11_MODULE=/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
# pkcs11-tool --keypairgen --key-type EC:prime256v1 --label "testkeyEC3333" --id 3333  --login --usage-sign
#

import os
import pkcs11

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.ec import encode_ec_public_key


message = b'A message to sign !'

lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
token = lib.get_token(token_label='SmartCard-HSM (UserPIN)')

print("sign:")
with token.open(rw=True, user_pin='123456') as session:
    priv   = session.get_key(label='testkeyEC3333', key_type=KeyType.EC, object_class=ObjectClass.PRIVATE_KEY)
    signature = priv.sign(message, mechanism=Mechanism.ECDSA_SHA256)

print("verify:")
with token.open(rw=True, user_pin='123456') as session:
    pubkey = session.get_key(label='testkeyEC3333', key_type=KeyType.EC, object_class=ObjectClass.PUBLIC_KEY)
    h = SHA256.new(message)
    verifier = DSS.new(ECC.import_key(encode_ec_public_key(pubkey)), 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("signature ok.")
    except ValueError:
        print("signature not ok!")
