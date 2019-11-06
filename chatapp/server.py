import socket, time, MySQLdb, threading

conn = MySQLdb.connect(host="localhost", user="root", database="chatapp")
cursor = conn.cursor()

serversocket = socket.socket()
serversocket.bind(("192.168.0.108",1234))
serversocket.listen(5)

c_users = []

class user:
	def __init__(self,username,password,c_socket,address):
		self.username = username
		self.password = password
		self.c_socket = c_socket
		self.address = address
#		self.status = 
	def login(self):
		querry = cursor.execute(f"SELECT * FROM user WHERE username='{self.username}' AND password='{self.password}'")
		data = cursor.fetchone()
		if  data == None or self.username != data[1]:
			return False
		return True
	def send_msg(self,msg):
		msg = "200:"+msg
		self.c_socket.send(bytes(msg, "utf-8"))

	def c_to_c_msg(self,other_c,msg):
		msg = 'chat:' + self.username+':'+msg
		other_c.c_socket.send(bytes(msg, 'utf-8'))

def check_user(chat_user):
	for user in c_users:
		if user.username == chat_user:
                        return user
	return False

def get_c_response(c_socket):
	try:
		res = c_socket.recv(1024)
		if res[:4].decode('utf-8') == "chat:":
			res = res.decode('utf-8').split(':')
			return res
		return res.decode('utf-8')
	except ConnectionResetError:
		print(f"connection from {c_users[-1].address} is closed")
		c_users.pop()
		c_socket.close()


def c_thread():
	c_socket, address = serversocket.accept()

	cred = get_c_response(c_socket)
	cred = cred.split()
	username = cred[0]
	password = cred[1]

	c_users.append(user(username,password,c_socket,address))

	if c_users[-1].login():
		c_users[-1].send_msg("Welcome to the server :)")

		print(f"connection from {c_users[-1].address} is successful ")
		time.sleep(10)
		c_users[-1].send_msg("1)Online Users\n2)Quit")

		request = get_c_response(c_socket)

		if request == '1':
			list_of_users = ", ".join([user.username for user in c_users])[::-1].replace(",", "& ",1)[::-1]
			c_users[-1].send_msg(list_of_users)
			chat_user = get_c_response(c_socket)
			chat_user = check_user(chat_user)
			if chat_user:

				#c_users[-1].send_msg("Connected with user ")
				while True:
					chat_user.send_msg(f"Chat request from {c_users[-1]}")
					resp = get_c_response(c_socket)
					print(resp)
					if resp:
						c_users[-1].c_to_c_msg(chat_user,resp)
					else:
						break
	c_users.pop()
	c_socket.close()


while True:

	t1 = threading.Thread(target=c_thread)
	t2 = threading.Thread(target=c_thread)
	t3 = threading.Thread(target=c_thread)
	t4 = threading.Thread(target=c_thread)
	t5 = threading.Thread(target=c_thread)

	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()

	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
