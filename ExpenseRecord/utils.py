import base64

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad


def hash_string(string, code):
    '''
        Hash a string with the code
    '''
    hash_obj = SHA256.new(code.encode('utf-8'))
    derived_key = hash_obj.digest()[:16]
    cipher = AES.new(derived_key, AES.MODE_CBC)

    # Padding plain text with padding bytes so that it is a multiple of 16 in length
    padded_plaintext = pad(string.encode('utf-8'), AES.block_size)

    # Encrypt padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # Concatenate the initialization vector (IV) and ciphertext
    iv_and_ciphertext = cipher.iv + ciphertext

    # Encode IV and ciphertext in base64 for storage and transmission
    encrypted = base64.b64encode(iv_and_ciphertext)

    # Convert to string to facilitate storage and transmission
    return encrypted.decode('utf-8')
