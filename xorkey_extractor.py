from FileDecryptor import FileDecryptor

PATH_TO_ENCRYPTED = "encrypted.lua"

if __name__ == '__main__':
    decryptor = FileDecryptor("")
    print(decryptor.decrypt_file(PATH_TO_ENCRYPTED, True))