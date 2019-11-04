

import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.connect(("127.0.0.1", 1234))

full_msg = ''

username = input("enter the username :")
password = input("enter the password :")

serversocket.send(bytes(username+' '+password, "utf-8"))
'''
while True:
	msg = serversocket.recv(1024)
	if len(msg) <= 0:
		break
	full_msg += msg.decode('utf-8')
print(full_msg)
'''

msg = serversocket.recv(1024)
print(msg.decode('utf-8'))
