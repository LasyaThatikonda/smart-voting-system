from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

key = hashlib.sha256(b"secret_key").digest()

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def encrypt_password(password):
    raw = pad(password)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(raw.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_password(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(enc).decode()
    return unpad(decrypted)