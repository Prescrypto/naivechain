# -*- encoding: utf-8 -*-

import rsa
import os
import string
import random
import hashlib
import merkletools
import cPickle
import binascii
import base64
import logging

# New cryptographic library
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

''' Basic functions and vars for genesis generation '''
def genesis_hash_generator(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

GENESIS_INIT_DATA = {
    "hashes" : [
        hashlib.sha256("chucho").hexdigest(),
        hashlib.sha256("cheve").hexdigest(),
        hashlib.sha256("bere").hexdigest(),
]}

def get_genesis_merkle_root():
    ''' Get first '''
    _mt = merkletools.MerkleTools()

    for single_hash in GENESIS_INIT_DATA["hashes"]:
        _mt.add_leaf(single_hash)
    _mt.make_tree();
    # get merkle_root and return
    return _mt.get_merkle_root();


class CryptoTools(object):
    ''' Object tools for encrypt and decrypt info '''
    
    def __init__(self):
        #This number is the entropy created by the user in FE, your default value is 161  
        self.ENTROPY_NUMBER = 161
        self.logger = logging.getLogger('django_info')

    def bin2hex(self, binStr): #OK
        '''convert str to hex '''
        return binascii.hexlify(binStr)
 
    def hex2bin(self, hexStr):#OK
        '''convert hex to str '''
        return binascii.unhexlify(hexStr)

    def savify_key(self, EncryptionKeyObject, is_legacy=True): #OK
        ''' Give it a key, returns a hex string ready to save '''
        if is_legacy:
            return self._savify_key(EncryptionKeyObject)
        else:
            pickld_key = EncryptionKeyObject.exportKey('PEM')
            return self.bin2hex(pickld_key)
     
    def _savify_key(self, EncryptionKeyObject):
        ''' Give it a key, returns a hex string ready to save '''
        # LEGAY METHOD
        pickld_key = cPickle.dumps(EncryptionKeyObject)
        return self.bin2hex(pickld_key)

    def un_savify_key(self, HexPickldKey, is_legacy=True): #OK
        ''' Give it a hex saved string, returns a Key object ready to use'''
        if is_legacy:
            return self._un_savify_key(HexPickldKey)
        else:
            bin_str_key = self.hex2bin(HexPickldKey)
            #return objetc of RSA type  
            return RSA.import_key(bin_str_key)
             
    def _un_savify_key(self, HexPickldKey):
        ''' Give it a hex saved string, returns a Key object ready to use  '''
        # LEGACY METHOD
        bin_str_key = self.hex2bin(HexPickldKey)
        return cPickle.loads(bin_str_key)

    def encrypt_with_public_key(self, message, EncryptionPublicKey, is_legacy=True): #OK
        ''' Encrypt with PublicKey object '''
        if is_legacy:
            return self._encrypt_with_public_key(message, EncryptionPublicKey)
        else:
            rsa_key = EncryptionPublicKey.exportKey('PEM')
            encrypt_rsa = Crypto.Cipher.PKCS1_OAEP.new(rsa_key)
            encryptedtext = encrypt_rsa.encrypt(message)
            return encryptedtext

    def _encrypt_with_public_key(self, message, EncryptionPublicKey):
        ''' Encrypt with PublicKey object '''
        # LEGACY METHOD
        encryptedtext=rsa.encrypt(message, EncryptionPublicKey)
        return encryptedtext

    def decrypt_with_private_key(self, encryptedtext, EncryptionPrivateKey, is_legacy=True):#OK
        ''' Decrypt with PrivateKey object '''
        if is_legacy:
            return self._decrypt_with_private_key(encryptedtext, EncryptionPrivateKey) 
        else:
            rsa_key = EncryptionPrivateKey.exportKey('PEM')
            decrypt_rsa = PKCS1_OAEP.new(rsa_key)
            message = decrypt_rsa.decrypt(encryptedtext)
            return message

    def _decrypt_with_private_key(self, encryptedtext, EncryptionPrivateKey):
        ''' Decrypt with PrivateKey object '''
        # LEGACY METHOD
        message =rsa.decrypt(encryptedtext, EncryptionPrivateKey)
        return message

    def sign(self, message, PrivateKey, is_legacy=True):#OK
        ''' Sign a message '''
        if is_legacy:
            return self._sign(message, PrivateKey)
        else:
            rsa_key = PrivateKey.exportKey('PEM')
            encrypt_rsa = RSA.import_key(rsa_key)
            message_hash = SHA256.new(message)
            signature = pkcs1_15.new(encrypt_rsa).sign(message_hash)
            return base64.b64encode(signature)

    def _sign(self, message, PrivateKey):
        ''' Sign a message '''
        # LEGACY METHOD
        signature = rsa.sign(message, PrivateKey, 'SHA-1')
        return base64.b64encode(signature)

    def verify(self, message, signature, PublicKey, is_legacy=True):#OK
        '''Verify if a signed message is valid'''
        if is_legacy:
            return self._verify(message, signature, PublicKey)
        else:
            signature = base64.b64decode(signature)
            rsa_key = PublicKey.exportKey('PEM')
            decrypt_rsa = RSA.import_key(rsa_key)
            message_hash = SHA256.new(message)
            try:
                pkcs1_15.new(decrypt_rsa).verify(message_hash, signature)
                return True   
            except Exception as e:
                self.logger.error("[CryptoTool, verify ERROR ] Signature or message are corrupted")
                return False

    def _verify(self, message, signature, PublicKey):
        '''Verify if a signed message is valid '''
        # LEGACY METHOD
        signature = base64.b64decode(signature)
        try:
            return rsa.verify(message, signature, PublicKey)
        except Exception as e:
            self.logger.error("[CryptoTool, verify ERROR ] Signature or message are corrupted")
            return False
