from flask import current_app
import hashlib
import binascii


# Keep in mind a secret key!
# if secret key is changed, all password for users is not working
# secret key is salt in hash pbkdf2_hmac

def hashing_sha256(password):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), current_app.config['SECRET_KEY'].encode(), 100000)
    return binascii.hexlify(dk).decode()


def check_hashing_sha256(password_hash, password):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), current_app.config['SECRET_KEY'].encode(), 100000)
    if binascii.hexlify(dk).decode() == password_hash:
        return True
    else:
        return False
