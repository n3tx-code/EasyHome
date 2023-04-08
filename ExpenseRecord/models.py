import base64

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExpenseRecord(models.Model):
    name = models.CharField(_("Nom"), max_length=255)
    users = models.ManyToManyField(User, related_name="expense_record")
    hashed_name = models.CharField(_("Nom chiffré"), max_length=255)  # representation of the name hashed with the unique code of the expense record

    def hash_name(self, code):
        '''
            Hash the name of the expense record with the code
        '''
        hash_obj = SHA256.new(code.encode('utf-8'))
        derived_key = hash_obj.digest()[:16]
        cipher = AES.new(derived_key, AES.MODE_CBC)

        # Padding plain text with padding bytes so that it is a multiple of 16 in length
        padded_plaintext = pad(self.name.encode('utf-8'), AES.block_size)

        # Encrypt padded plaintext
        ciphertext = cipher.encrypt(padded_plaintext)

        # Concatenate the initialization vector (IV) and ciphertext
        iv_and_ciphertext = cipher.iv + ciphertext

        # Encode IV and ciphertext in base64 for storage and transmission
        encrypted = base64.b64encode(iv_and_ciphertext)

        # Convert to string to facilitate storage and transmission
        self.hashed_name = encrypted.decode('utf-8')
        self.save()

    def check_code(self, key):
        '''
            Check if the code is the good one
        '''
        hash_obj = SHA256.new(key.encode('utf-8'))
        derived_key = hash_obj.digest()[:16]

        # Decode ciphertext from base64
        encrypted = base64.b64decode(self.hashed_name)

        # Retrieve initialization vector (IV) from first 16 bytes
        iv = encrypted[:AES.block_size]

        # Retrieve ciphertext from remaining bytes
        ciphertext = encrypted[AES.block_size:]

        # Initialize decryptor with derived key and IV
        cipher = AES.new(derived_key, AES.MODE_CBC, iv)

        # Decrypt ciphertext
        padded_plaintext = cipher.decrypt(ciphertext)

        try:
            # Remove padding bytes added during encryption
            plaintext = unpad(padded_plaintext, AES.block_size).decode('utf-8')
        except ValueError:
            return False

        return plaintext == self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense record"
        verbose_name_plural = "Expense ecords"
