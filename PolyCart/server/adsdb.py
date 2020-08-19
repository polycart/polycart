import sqlite3

class AdsDataBase:
	def __init__(self):
		self.database = sqlite3.connect('ads.db', check_same_thread = False)
		self.c = self.database.cursor()
		
		try:
			self.c.execute("""create table ads
				(number integer primary key,
				name text,
				image text,
				pos_x real,
				pos_y real)""")
		except:
			pass


	def insert(self, number, name, image, pos_x, pos_y):
		try:
			self.c.execute("insert into ads values (?, ?, ?, ?, ?)",(number, name, image, pos_x, pos_y))
			self.database.commit()
		except:
			return False
		else:
			return True

	def select(self, number):
		try:
			self.c.execute("select code, name, image, price, pos_x, pos_y, number from ads where number = ?", (number,))
		except:
			return None
		else:
			return self.c.fetchone()

	def has(self, number):
		if self.select(number) != None:
			return True
		else: return False

	def getlist(self):
		try:
			self.c.execute("select name, image, pos_x, pos_y from ads")
		except:
			return None
		else:
			return self.c.fetchall()

	def delete(self, number):
		try:
			self.c.execute("select name from ads where number = ?", (number,))
			if self.c.fetchone() == None:
				return True
			self.c.execute("delete from ads where number = ?", (number,))
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
db = AdsDataBase()

print(db.insert('3127546', 'Chen_Py', 'cd.jpg', 2, 2))

print(db.insert('3127547', 'Chen', 'cd.jpg', 2, 2))

print(db.insert('3127548', 'aha_Chen_Py_CCCpy', 'cd.jpg', 2, 2))

print(db.insert('3127549', 'CPY', 'cd.jpg', 2, 2))

print(db.getlist())
'''