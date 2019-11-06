
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.connect(("192.168.0.108", 1234))

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
def chat(otheruser, msg):

	while True:
		print(msg)
		message = input(f"enter the msg to chat with {otheruser} :")
		#print(message)
		#chat(c_name,message)
		serversocket.send(bytes("chat:"+otheruser+':'+message, 'utf-8'))
		response = validate_response()
		print(response)
		if response[0] != 'chat':
			print("chat closed by server ")
			serversocket.close()
			exit()


def validate_response():
	msg = serversocket.recv(1024)
	msg = msg.decode('utf-8').split(':')
	if msg[0]=='chat':
		chat(msg[1],msg[2])
		print(msg)
		#print(f'{msg[1]}:{msg[-1]}')
		return msg
	elif msg[0] != "200":
		print("Connection closed by the server")
		serversocket.close()
		exit()
	return msg[-1]

print(validate_response()) # receving welcome message from server

 # receving choice from server
print(validate_response())
request = input("enter your choice: ")
serversocket.send(bytes(request,'utf-8')) # sending choice to server

# receving result of requested choice by client
print(validate_response())

c_name = input("enter the client name:")
serversocket.send(bytes(c_name, 'utf-8'))

print(validate_response())

x = input('enter the msg you want to send: ')
serversocket.send(bytes(x, 'utf-8'))
chat(c_name, x)
