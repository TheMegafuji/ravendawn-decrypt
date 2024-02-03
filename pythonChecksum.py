import zlib

file = "init.lua"

with open(file, 'rb') as random_file:
    data = random_file.read()

crc32_checksum = zlib.crc32(data)
crc32_checksum_hex = format(crc32_checksum & 0xFFFFFFFF, '08x')

print(crc32_checksum_hex)
