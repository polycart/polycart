import pyDes
from hashlib import blake2b

def encrypt(data, key, iv):
    iv = iv.to_bytes(8, 'big')
    key = key.to_bytes(24, 'big')
    data = data.encode()
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    res = k.encrypt(data)
    return res
    
def decrypt(data, key, iv):
    iv = iv.to_bytes(8, 'big')
    key = key.to_bytes(24, 'big')
    k = pyDes.triple_des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    res = k.decrypt(data)
    res = res.decode()
    return res

def hash(data):
	myhash = blake2b(digest_size = 24)
	myhash.update(data.encode('utf-8'))
	num = myhash.hexdigest()
	num = int('0x' + num, 16)
	return num

def Pow(n, a, mod):
	if(a == 0):
		return 1
	if(a % 2 == 1):
		return (n * Pow(n, a-1, mod)) % mod
	if(a % 2 == 0):
		temp = Pow(n, a/2, mod)
		return (temp * temp) % mod

def Make_Private_Code(N, m, Private_Secret_Code):
	P = Pow(N, Private_Secret_Code, m)
	Private_Open_Code = (N, m, P)
	return (Private_Open_Code, Private_Secret_Code)

def Make_Communication_Code(Private_Open_Code, Communication_Secret_Code):
	N = Private_Open_Code[0]
	m = Private_Open_Code[1]
	P = Private_Open_Code[2]
	Communication_Open_Code = Pow(N, Communication_Secret_Code, m)
	Key = Pow(P, Communication_Secret_Code, m)
	return (Communication_Open_Code, Communication_Secret_Code, Key)

def Make_Key(Communication_Open_Code, m, Private_Secret_Code):
	Key = Pow(Communication_Open_Code, Communication_Secret_Code, m)
	return Key