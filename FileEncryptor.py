import lzma
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

from KeyHandler import KeyHandler

class FileEncryptor:
    def __init__(self, data_path):
        self.data_path = data_path

    def evp_encrypt(self, key, plaintext, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return ciphertext

    def encrypt_file(self, file_path, xor_key, random_noise):
        file_name = os.path.basename(file_path)
        keyHandler = KeyHandler()
        key = keyHandler.get_key(keyHandler.get_xor_file(file_name), xor_key)
        iv = keyHandler.get_iv(file_name, xor_key)
        
        with open(file_path, 'rb') as file:
            plaintext = file.read()
            compressed_data = lzma.compress(plaintext)
            encrypted_data = self.evp_encrypt(key[:32], compressed_data, iv)

        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(random_noise)
            encrypted_file.write(encrypted_data)

    def encrypt_all_files(self, xor_key, random_noise):
        for root, _, files in os.walk(self.data_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.encrypt_file(file_path, xor_key, random_noise)
