from socket import *
from crypto import *
from threading import Thread

alliv = 1772048404007700507

class ServerBase(Thread):
	def __init__(self, clisocket, ip):
		Thread.__init__(self)
		self.clisock = clisocket
		self.usname = None
		self.logged = False
		self.ip = ip
		self.bufsiz = 1024

	# server methods
	def Welcome(self):
		print("Welcome to Server")
		self.clisock.send('Welcome to Server'.encode())
	
	# send error
	def Error(self, mark):
		msg = mark + 'is not an avaliable mark'
		self.clisock.send(msg.encode())

	def run(self):
		while True:
			try:
				mark = self.clisock.recv(self.bufsiz).decode()
			except:
				print('logout')
				break
			else:
				try:
					if mark == 'WEL':
						self.Welcome()
					else:
						self.Error(mark)
				except:
					print('logout')
					break
		self.clisock.close()





def run(host = '172.17.136.87', port = 21567, bufsiz = 1024, lissiz = 5):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(lissiz)
	print('Waiting...')
	while True:
		try:
			clisock, addr = sock.accept()
			print('...receive from' + str(addr))
			SB = ServerBase(clisock, addr[0])
			SB.start()
		except:
			print('error')
			continue
	sock.close()

run()