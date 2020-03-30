from clientbase.clientsocket import TcpCliSock
from clientbase.crypto import *
import time
class ClientBase:
	def __init__(self):
		self.clisock = TcpCliSock()
		self.key = None
		self.name = None
		self.logged = False
		self.allm = 6277101735386680763835789423207666416102355444464034512659
		self.alliv = 1772048404007700507
		pass

	def userstr(self, name, password):
		Private_Code = Make_Private_Code(hash(name), self.allm, hash(password))[0]
		return name + ': ' + str(Private_Code) + '\n'

	def NewUser(self, name, password):
		if self.clisock.state != 'Connected' or name == '' or password == '':
#			print('Unsuccessful')
			return False
		msg = self.userstr(name, password)
		try:
			self.clisock.send('NUS', msg)
			res = self.clisock.recvstr()
#			print(res)
		except:
			return False
		if(res != 'Creat Successfully'):
			return False
		return True

	def LogIn(self, name, password):
		if self.clisock.state != 'Connected' or name == '' or password == '':
#			print('Unsuccessful')
			return False
		try:
			self.clisock.send('AFT', name)
			msg = self.clisock.recvbyte()
			if(msg == b'Unsuccessful'):
#				print('Unsuccessful')
				return False
			Communication_Open_Code = int(123).from_bytes(msg, 'big')
			ip = self.clisock.recvstr()
			self.key = Make_Key(Communication_Open_Code, self.allm, hash(password))
			msg = encrypt(ip, self.key, self.alliv)
			self.clisock.send('RTT', msg)
			res = self.clisock.recvbyte()
		except:
			return 'Unsuccessful'
		if res == b'Unsuccessful':
#			print("Unsuccessful")
			return False
		if(decrypt(res, self.key, self.alliv) != 'Sign In Successfully'):
			return False
#		print(decrypt(res, self.key))
		self.name = name
		self.logged = True
		return True

	def ChangePassword(self, new_password):
		if self.clisock.state != 'Connected' or self.logged == False or new_password == '':
#			print("Unsuccessful")
			return False
		try:
			msg = self.userstr(self.name, new_password)
			msg = encrypt(msg, self.key, self.alliv)
			self.clisock.send('CPC', msg)
			res = self.clisock.recvbyte()
		except:
#			print('Unsuccessful')
			return False
		if res == b'Unsuccessful':
#			print('Unsuccessful')
			return False
		try: 
			if(decrypt(res, self.key, self.alliv) != 'Change Successfully'):
#				print("Unsuccessful ")
				return False
		except:
#			print('Unsuccessful')
			return False
#		print('Change Successfully')
		return True

	def DeletUser(self):
		if self.clisock.state != 'Connected' or self.logged == False:
#			print('Unsuccessful')
			return False
		try:
			msg = encrypt(self.name, self.key, self.alliv)
			self.clisock.send('DUS', msg)
			res = self.clisock.recvbyte()
			if res == b'Unsuccessful':
#				print('Unsuccessful')
				return False
		except:
#			print('Unsuccessful')
			return False
		if(decrypt(res, self.key, self.alliv) != 'Delete Successfully'):
			return False
#		print('Delete %s Successfully' %self.name)
		return True

	def SearchForGoods(self, name):
		if self.clisock.state != 'Connected':
			return False
		try:
			self.clisock.send('SFG', name.encode())
			num = int(self.clisock.recvstr())
			reslist = []
			for i in range(num):
				msg = self.clisock.recvstr()
				print(msg)
				reslist.append(eval(msg))
		except:
			return False
		else:
			return reslist