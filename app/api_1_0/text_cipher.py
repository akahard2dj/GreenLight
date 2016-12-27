import binascii

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class RSACipher:
    def __init__(self, private_key_file):
        with open(private_key_file, 'rb') as key_file:
            self.__private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def decrypt(self, ciphertext):
        plaintext = self.__private_key.decrypt(
            binascii.unhexlify(ciphertext.encode()),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext.decode()

'''
class RSACipher:
    def __init__(self, private_key_file):
        print('called')
        with open(private_key_file, mode='rb') as priv_file:
            keydata = priv_file.read()
            self.__priv_key = rsa.PrivateKey.load_pkcs1(keydata)

    def decrypt(self, crypto):
        message = rsa.decrypt(binascii.unhexlify(crypto.encode()), self.__priv_key)

        return message.decode()

class TextCipher:
    def __init__(self, key):
        self.bs = 32
        self.key = base64.b64encode(self._pad(key).encode())

    def encryption(self, text):
        f = Fernet(self.key)
        if isinstance(text, str):
            token = f.encrypt(text.encode())
            return token
        else:
            return None

    def decryption(self, cipher_text):
        f = Fernet(self.key)
        return f.decrypt(cipher_text.encode()).decode()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
'''