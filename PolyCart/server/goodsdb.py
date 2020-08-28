import sqlite3

class GoodsDataBase:
	def __init__(self):
		self.database = sqlite3.connect('goods.db', check_same_thread = False)
		self.c = self.database.cursor()
		
		try:
			self.c.execute("""create table goods
				(code text primary key,
				name text,
				image text,
				weight real,
				price real,
				pos_x real,
				pos_y real,
				number integer)""")
		except:
			pass


	def insert(self, code, name, image, weight, price, pos_x, pos_y):
		try:
			self.c.execute("insert into goods values (?, ?, ?, ?, ?, ?, ?, ?)",(code, name, image, weight, price, pos_x, pos_y, 0))
			self.database.commit()
		except Exception as e:
			print(str(e))
			return False
		else:
			return True

	def select(self, code):
		try:
			self.c.execute("select code, name, image, price, pos_x, pos_y, number, weight from goods where code = ?", (code,))
		except:
			return None
		else:
			return self.c.fetchone()

	def search(self, name):
		name = '%' + name + '%'
		try:
			self.c.execute("select name, image, price, pos_x, pos_y from goods where name like ?", (name,))
		except:
			return []
		else:
			reslist = self.c.fetchall()
			return reslist

	def has(self, code):
		if self.select(code) != None:
			return True
		else: return False

	def modify_number(self, code, new_number):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update goods set number = ? where code = ?", (new_number, code))
			self.database.commit()
		except:
			return False
		else:
			return True

	def modify_name(self, code, new_name):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update goods set name = ? where code = ?", (new_name, code))
			self.database.commit()
		except:
			return False
		else:
			return True

	def modify_price(self, code, new_price):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update goods set price = ? where code = ?", (new_price, code))
			self.database.commit()
		except:
			return False
		else:
			return True

	def modify_pos(self, code, new_pos):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update goods set pos_x = ?, pos_y = ? where code = ?", (new_pos[0], new_pos[1], code))
			self.database.commit()
		except:
			return False
		else:
			return True

	def modify_image(self, code, new_image):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return False
			self.c.execute("update goods set image = ? where code = ?", (new_image, code))
			self.database.commit()
		except:
			return False
		else:
			return True

	def delete(self, code):
		try:
			self.c.execute("select name from goods where code = ?", (code,))
			if self.c.fetchone() == None:
				return True
			self.c.execute("delete from goods where code = ?", (code,))
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
db = GoodsDataBase()
print(db.search('Chen'))
print(db.insert('3127546', 'Chen_Py', 'cd.jpg', 3.5, 2, 2))

print(db.insert('3127547', 'Chen', 'cd.jpg', 3.5, 2, 2))

print(db.insert('3127548', 'aha_Chen_Py_CCCpy', 'cd.jpg', 3.5, 2, 2))

print(db.insert('3127549', 'CPY', 'cd.jpg', 3.5, 2, 2))
'''