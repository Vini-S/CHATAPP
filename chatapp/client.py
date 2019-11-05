
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.connect(("192.168.0.121", 1234))

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

msg = serversocket.recv(1024) # receing welcome message from server
if msg.decode('utf-8') == '':
	print("Invalid user")
	exit()
else:
	print(msg.decode('utf-8'))

choice = serversocket.recv(1024) # receving choice from server
print(choice.decode('utf-8'))
request = input("enter your choice: ")
serversocket.send(bytes(request,'utf-8')) # sending choice to server

result = serversocket.recv(1024) # receving result of requested choice by client
print(result.decode('utf-8'))

c_name = input("enter the client name:")
serversocket.send(bytes(c_name, 'utf-8'))
