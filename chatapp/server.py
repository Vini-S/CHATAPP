import socket, time, MySQLdb, threading

conn = MySQLdb.connect(host="localhost", user="root", database="chatapp")
cursor = conn.cursor()
#cursor.execute("SELECT * FROM user")
#data = cursor.fetchall()
#print(data)

serversocket = socket.socket()

serversocket.bind(("192.168.0.121",1234))

serversocket.listen(5)

c_users = []

class user:
	def __init__(self,username,password,c_socket,address):
		self.username = username
		self.password = password
		self.c_socket = c_socket
		self.address = address
	def login(self):
		querry = cursor.execute(f"SELECT * FROM user WHERE username='{self.username}' AND password='{self.password}'")
		data = cursor.fetchone()
		if  data != None and self.username == data[1]:
			return True
	def send_msg(self,msg):
		self.c_socket.send(bytes(msg, "utf-8"))


def c_thread():
	c_socket, address = serversocket.accept()
	cred = c_socket.recv(1024)
	cred = cred.split()
	username = cred[0].decode('utf-8')
	password = cred[1].decode('utf-8')

	#clientsocket.send(bytes("WELCOME TO THE SERVER", "utf-8"))

	c_users.append(user(username,password,c_socket,address))

	if c_users[-1].login():
		c_users[-1].send_msg("Welcome To the Server :)")

		print(f"connection from {c_users[-1].address} is successful ")

		c_users[-1].send_msg("1)Online Users \n2)Quit\n")

		request = c_socket.recv(1024)
		if int(request.decode('utf-8')) == 1:
			list_of_users = ", ".join([user.username for user in c_users])[::-1].replace(",", "& ",1)[::-1]
			c_socket.send(bytes(list_of_users, 'utf-8'))
			chat_user = c_socket.recv(1024)
			print(chat_user)
	c_users.pop()
	c_socket.close()


while True:
	t1 = threading.Thread(target=c_thread)
	t2 = threading.Thread(target=c_thread)
	t1.start()
	t2.start()
	t1.join()
	t2.join()
