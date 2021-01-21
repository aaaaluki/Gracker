memory = "0x6d616e75	0x612d2065"

memoryArr = memory.replace('0x', '').split("\t")

final = ''

for mem in memoryArr:
    temp = bytearray.fromhex(mem).decode()
    final = final + temp[::-1]

print(f'String stored: {final}')