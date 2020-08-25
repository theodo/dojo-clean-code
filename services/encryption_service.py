# AES 256 encryption/decryption using pycryptodome library

import json
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES


def encrypt(data, password):
    plain_text = json.dumps(data)

    # use the SHA256 algorithm to get a private key from the password
    private_key = hashlib.sha256(password.encode()).digest()

    # create cipher config
    cipher = AES.new(private_key, AES.MODE_CFB)
    ciphered_data = cipher.encrypt(bytes(plain_text, 'utf-8'))
    encoded_data = bytearray(cipher.iv) + bytearray(ciphered_data)

    return b64encode(encoded_data).decode('utf-8')


def decrypt(encoded_cipher, password):
    # use the SHA256 algorithm to get a private key from the password
    private_key = hashlib.sha256(password.encode()).digest()

    decoded_cipher = bytearray(b64decode(encoded_cipher))
    iv = decoded_cipher[:16]
    cipher = decoded_cipher[16:]

    cipher_config = AES.new(private_key, AES.MODE_CFB, iv=iv)
    plain_text = bytes.decode(cipher_config.decrypt(cipher))
    return json.loads(plain_text)


if __name__ == "__main__":
    password = input("Password: ")

    # First let us encrypt secret message
    encrypted = encrypt([], password)
    print(encrypted)

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, password)
    print(decrypted)
