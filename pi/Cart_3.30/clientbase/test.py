from clientbase import ClientBase
cpy = ClientBase()
print(cpy.clisock.state)
print(cpy.NewUser('Chen_Py', '123'))
print(cpy.NewUser('CPY', '456'))

while True:
	a = str(input('name >>> '))
	if(a == 'exit'):
		break
	b = str(input('password >>> '))
	if cpy.LogIn(a, b):
		print('True')
		break
	print('False')
c = str(input('password>>>'))
print(cpy.ChangePassword(c))
cpy.DeletUser()
cpy.clisock.close()
