###
# cryption.py
# contains functions vital for encrypting/decrypting request data.
###

import base64
import hashlib
import hmac
import json
import os
import time
import uuid

from Crypto.Cipher import AES

import config

# Padding for the input string --not
# related to encryption itself.

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def generate_unique_id() -> str:
    rnd_uuid = str(uuid.uuid4())
    rnd_unique_id = str(uuid.uuid4()) + ':' + rnd_uuid[0:8]
    return rnd_unique_id


# thanks to renzy for assisting on how the identifier & Basic works so that i could write this. - k1mpl0s
def basic(identifier):
    if ':' not in identifier:
        # remove next-lines
        if '\n' in identifier:
            temp = identifier.replace('\n', '')
        else:
            temp = identifier
        # append blanks to make size of 160
        if len(temp) < 159:
            while len(temp) < 159:
                temp = temp.ljust(159, '\u0008')
        # flip identifier
        decode = base64.b64decode(temp).decode()
        part = decode.split(':')
        temp = part[1] + ':' + part[0]
    else:
        # flip identifier
        part = identifier.split(':')
        temp = part[1] + ':' + part[0]
    # basic
    return base64.b64encode(temp.encode()).decode()


def mac(method, action):
    ts = str(int(round(time.time(), 0)))
    nonce = ts + ':' + str(hashlib.md5(ts.encode()).hexdigest())
    value = ts + '\n' + nonce + '\n' + method + '\n' + action + '\n' \
            + config.game_env.url.replace('https://', '') + '\n' + str(config.game_env.port) + '''

'''
    secret = config.game_account.secret.encode('utf-8')
    hmac_hex_bin = hmac.new(secret, value.encode('utf-8'), hashlib.sha256).digest()
    mac = base64.b64encode(hmac_hex_bin).decode()
    final = 'MAC ' + 'id=' + '"' + config.game_account.access_token + '"' + ' nonce=' + '"' \
            + nonce + '"' + ' ts=' + '"' + ts + '"' + ' mac=' + '"' + mac \
            + '"'
    return final


def get_key_and_iv(
    password,
    salt,
    klen=32,
    ilen=16,
    msgdgst='md5',
):
    '''
    Derive the key and the IV from the given password and salt.

    This is a niftier implementation than my direct transliteration of
    the C++ code although I modified to support different digests.

    CITATION: http://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python

    @param password  The password to use as the seed.
    @param salt      The salt.
    @param klen      The key length.
    @param ilen      The initialization vector length.
    @param msgdgst   The message digest algorithm to use.
    '''

    # equivalent to:
    #   from hashlib import <mdi> as mdf
    #   from hashlib import md5 as mdf
    #   from hashlib import sha512 as mdf

    mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
    password = password.encode('ascii', 'ignore')  # convert to ASCII

    try:
        maxlen = klen + ilen
        keyiv = mdf(password + salt).digest()
        tmp = [keyiv]
        while len(tmp) < maxlen:
            tmp.append(mdf(tmp[-1] + password + salt).digest())
            keyiv += tmp[-1]  # append the last byte
        key = keyiv[:klen]
        iv = keyiv[klen:klen + ilen]
        return (key, iv)
    except UnicodeDecodeError:
        return (None, None)


def encrypt_sign(data):
    data = pad(data)
    key1 = str.encode(data)
    password = 'iyMgxvi240Smc5oPikQugi0luUp8aQjcxMPO27n7CyPIIDZbfQbEgpWCYNHSTHB'
    salt = os.urandom(8)
    (key, iv) = get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    a = cipher.encrypt(key1)
    a = salt + a
    return base64.b64encode(a).decode()


def decrypt_sign(sign):
    buffer = base64.b64decode(sign)
    password = 'iyMgxvi240Smc5oPikQugi0luUp8aQjcxMPO27n7CyPIIDZbfQbEgpWCYNHSTHB'
    salt = buffer[0:8]
    (key, iv) = get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5')
    data = buffer[8:len(buffer)]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    a = unpad(cipher.decrypt(data)).decode('utf8')
    return json.loads(a)
