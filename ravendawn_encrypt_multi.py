from FileEncryptor import FileEncryptor

random_noise_path = "random.bin"
xor_key = 50

with open(random_noise_path, 'rb') as random_file:
    random_noise = random_file.read()

if __name__ == '__main__':
    data_path = 'game_bot'
    encryptor = FileEncryptor(data_path)
    encryptor.encrypt_all_files(xor_key, random_noise)