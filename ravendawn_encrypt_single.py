from FileEncryptor import FileEncryptor

PATH_TO_DECRYPTED = "init.lua"
random_noise_path = "random.bin"
xor_key = 50

with open(random_noise_path, 'rb') as random_file:
    random_noise = random_file.read()

if __name__ == '__main__':
    encryptor = FileEncryptor("")
    encryptor.encrypt_file(PATH_TO_DECRYPTED, xor_key, random_noise)