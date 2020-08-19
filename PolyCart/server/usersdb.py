import sqlite3

class UsersDataBase:
	def __init__(self):
		self.database = sqlite3.connect('users.db', check_same_thread = False)
		self.c = self.database.cursor()
		
		try:
			self.c.execute("""create table users
				(name text primary key,
				N text,
				m text,
				P text)""")
		except:
			pass


	def insert(self, name, N, m, P):
		N = str(N)
		m = str(m)
		P = str(P)
		try:
			self.c.execute("insert into users values (?, ?, ?, ?)",(name, N, m, P))
			self.database.commit()
		except:
			return False
		else:
			return True

	def select(self, name):
		try:
			self.c.execute("select N, m, P from users where name = ?", (name,))
		except:
			return None
		else:
			N, m, P = self.c.fetchone()
			N = int(N)
			m = int(m)
			P = int(P) 
			return N, m, P

	def has(self, name):
		if self.select(name) != None:
			return True
		else: return False

	def modify(self, name, N, m, P):
		N = str(N)
		m = str(m)
		P = str(P)
		try:
			self.c.execute("select name from users where name = ?", (name,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update users set N = ?, m = ?, P = ? where name = ?", (N, m, P, name))
			self.database.commit()
		except:
			return False
		else:
			return True

	def delete(self, name):
		try:
			self.c.execute("select name from users where name = ?", (name,))
			if self.c.fetchone() == None:
				return True
			self.c.execute("delete from users where name = ?", (name, ))
			self.database.commit()
		except:
			return False
		else:
			return True

	def close(self):
		self.database.commit()
		self.database.close()
		pass
'''
datab = UsersDataBase()
print(datab.insert('chen', 2, 3, 4))
print(datab.ask('chen'))
print(datab.modify('chen', 1, 2, 3))
print(datab.ask('chen'))
print(datab.delete('chen'))
print(datab.ask('chen'))
datab.close()
'''