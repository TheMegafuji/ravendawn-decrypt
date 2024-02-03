from OpenSSL import crypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import lzma
import os
from zipfile import ZipFile

from KeyHandler import KeyHandler

class FileDecryptor:
    def __init__(self, data_path):
        self.data_path = data_path

    def evp_decrypt(self, key, ciphertext, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext

    def get_xor_key(self, file_data, keyHandler: KeyHandler):
        return keyHandler.get_bytes(file_data[5] ^ 0x1337)

    def decrypt_file(self, file_path, extract_keys = False):
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as encrypted_file:
            if encrypted_file.read(4) != b'P00P':
                print("Not poop, skipping: " + file_path)
                return
            encrypted_file.seek(0)
            keyHandler = KeyHandler()
            xor_key = self.get_xor_key(bytearray(encrypted_file.read()), keyHandler)
            key = keyHandler.get_key(keyHandler.get_xor_file(file_name), xor_key)
            iv = keyHandler.get_iv(file_name, xor_key)

            if extract_keys:
                return xor_key

        with open(file_path, 'rb') as file:
            random_noise = file.read(16)
            if extract_keys:
                with open('random.bin', 'wb') as key_file:
                    key_file.write(random_noise)
            decompressed = lzma.decompress(self.evp_decrypt(key[:32], file.read(), iv))

        with open(file_path, 'wb') as new:
            new.write(decompressed)

    def decrypt_all_files(self):
        for root, _, files in os.walk(self.data_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.decrypt_file(file_path)