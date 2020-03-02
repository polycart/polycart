from socket import *
import time
class TcpCliSock:
	def __init__(self, host = '39.96.48.80', port = 21567, bufsiz = 1024):
		
		self.host = host
		self.port = port
		self.bufsiz = bufsiz
		self.sock = socket(AF_INET, SOCK_STREAM)
		
		try:
			self.sock.connect((host, port))
		except ConnectionRefusedError:
			self.state = 'Refused'
		except TimeoutError:
			self.state = 'TimeOut'
		else:
			self.state = 'Connected'


	def send(self, sign, data):
		if(self.state != 'Connected'):
			return False
		self.sock.send(sign.encode())
		time.sleep(0.1)
		if data == None: return True
		if(isinstance(data, str)):
			self.sock.send(data.encode())
		else:
			self.sock.send(data)
		return True

	def recvstr(self):
		if(self.state != 'Connected'):
			return None
		return self.sock.recv(self.bufsiz).decode()

	def recvbyte(self):
		if(self.state != 'Connected'):
			return None
		return self.sock.recv(self.bufsiz)

	def close(self):
		self.sock.close()

