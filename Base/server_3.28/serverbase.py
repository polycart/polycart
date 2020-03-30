import time
import secrets
from socket import *
from crypto import *
from threading import Thread
from usersdb import UsersDataBase
from goodsdb import GoodsDataBase

class ServerBase(Thread):
	def __init__(self, clisocket, ip):
		Thread.__init__(self)
		self.clisock = clisocket
		self.usname = None
		self.logged = False
		self.loggint = False
		self.ip = ip
		self.bufsiz = 1024
		self.alliv = 1772048404007700507
		self.database = UsersDataBase()
		self.goodsdb = GoodsDataBase()

	def user(self, string):
		name, Private_Code = string[0:-1].split(': ')
		Private_Code = Private_Code[1:-1].split(', ')
		for i in range(0,3):
			Private_Code[i] = int(Private_Code[i])
		Private_Code = tuple(Private_Code)
		return name, Private_Code

	def SendError(self):
		try:
			self.clisock.send('Unsuccessful'.encode())
		except:
			print('SendError Error')
		pass

	# server methods
	def Welcome(self):
		print("Welcome to Server")
		self.clisock.send('Welcome to Server'.encode())
	
	def NewUser(self):
		try:
			msg = self.clisock.recv(self.bufsiz).decode()
			name, Private_Code = self.user(msg)
		except:
			self.SendError()
			return
		addres = self.database.insert(name, Private_Code[0], Private_Code[1], Private_Code[2])
		if not addres:
			self.SendError()
		else:
			self.clisock.send('Creat Successfully'.encode())
		pass

	def LoginTest(self):
		self.logging = True
		try:
			self.usname = self.clisock.recv(self.bufsiz).decode()
		except ConnectionResetError:
			self.logging = False
			return
		if not self.database.has(self.usname):
			self.SendError()
			self.logging = False
			return
		Private_Code = self.database.select(self.usname)
		self.test = secrets.token_hex(24)
		self.test = int('0x' + self.test, 16)
		coc, csc, self.key = Make_Communication_Code(Private_Code, self.test)
		msg = coc.to_bytes(24, 'big')
		self.clisock.send(msg)
		time.sleep(0.1)
		self.clisock.send(self.ip.encode())
		pass

	def LoginCheck(self):
		if not self.logging:
			self.clisock.recv(self.bufsiz)
			SendError()
			return
		try:
			ip = self.clisock.recv(self.bufsiz)
		except:
			SendError()
			self.logging = False
			return
		if ip == encrypt(self.ip, self.key, self.alliv):
			self.logged = True
			self.clisock.send(encrypt('Sign In Successfully', self.key, self.alliv))
			self.logging = False
			return
		else:
			self.SendError() 
			self.logging = False
			return

	def ChangePassword(self):
		if not self.logged:
			self.clisock.recv(self.bufsiz)
			self.SendError()
			return
		msg = self.clisock.recv(self.bufsiz)
		msg = decrypt(msg, self.key, self.alliv)
		name, Private_Code = self.user(msg)
		if name != self.usname:
			self.SendError()
			return
		if not self.database.modify(name, Private_Code[0], Private_Code[1], Private_Code[2]):
			self.SendError()
			return
		msg = encrypt('Change Successfully', self.key, self.alliv)
		self.clisock.send(msg)
		return

	def DelUser(self):
		if not self.logged: 
			self.SendError()
			pass
		name = self.clisock.recv(self.bufsiz)
		name = decrypt(name, self.key, self.alliv)
		if name != self.usname:
			self.SendError()
			return
		if self.database.delete(name):
			msg = encrypt('Delete Successfully', self.key, self.alliv)
			self.clisock.send(msg)
			self.usname = None
			self.logged = False
			return
		else:
			self.SendError()
			return

	def SearchForGoods(self):
		name = self.clisock.recv(self.bufsiz).decode()
		reslist = self.goodsdb.search(name)
		self.clisock.send(str(len(reslist)).encode())
		for one in reslist:
			time.sleep(0.1)
			self.clisock.send(str(one).encode())
		pass

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
					elif mark == 'NUS':
						self.NewUser()
					elif mark == 'AFT':
						self.LoginTest()
					elif mark == 'RTT':
						self.LoginCheck()
					elif mark == 'CPC':
						self.ChangePassword()
					elif mark == 'DUS':
						self.DelUser()
					elif mark == 'SFG':
						self.SearchForGoods()
					else:
						self.Error(mark)
				except:
					print('logout')
					break
		self.database.close()
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