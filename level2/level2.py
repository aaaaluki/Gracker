#!/usr/bin/env python3

from itertools import cycle

encrypted = ")q6\036(2\036\065)p2\036)u\"*r3\036'q--q6(/&\036,r"
key = 'A'

encoding = 'utf-8'

decrypted = [e ^ k for (e, k) in zip(bytes(encrypted, encoding), cycle(bytes(key, encoding)))]
password = ''.join([chr(i) for i in decrypted])

print(f'Password: {password}\nAscii values: {decrypted}')
