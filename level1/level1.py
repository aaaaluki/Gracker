#!/usr/bin/env python3

from itertools import cycle

encrypted = '/q#q%8\036&4r22$2\036\065)(t\036\061 226q3%'
key = 'A'

encoding = 'utf-8'

decrypted = [e ^ k for (e, k) in zip(bytes(encrypted, encoding), cycle(bytes(key, encoding)))]
password = ''.join([chr(i) for i in decrypted])

print(f'Password: {password}\nAscii values: {decrypted}')
