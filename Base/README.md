# Base 介绍

**Base**文件夹下包含PolyCart项目内的一些底层代码

## clientsocket.py

用于客户端的套接字，使用TCP协议

> 套接字（socket）是一个抽象层，应用程序可以通过它发送或接收数据，可对其进行像对文件一样的打开、读写和关闭等操作。套接字允许应用程序将I/O插入到网络中，并与网络中的其他应用程序进行通信。网络套接字是IP地址与端口的组合。

---

### TcpCliSock

客户端通信类

**构造函数：** *TcpCliSock(host = “175.24.57.48”, port = 21567, bufsiz = 1024)*

---

### TcpCliSock.host

连接到的主机地址，类型为**string**。例如：*“175.24.57.48”*

---

### TcpCliSock.port

程序通信的端口，类型为**int**。默认为：*21567*

---

### TcpCliSock.bufsiz

接收信息最大长度，类型为**int**，单位为**Byte**。默认为：*1024*

---

### TcpCliSock.state

连接状态，类型为**string**。

* Connected：表示套接字成功连接，可以进行通信

* Refused：表示套接字连接请求被拒绝

* TimeOut：表示套接字连接请求超时，可能因自身或服务器的网络问题导致

当**state**状态为**Connected**时，可以发送信息，否则不可发送。

---

### TcpCliSock.send(sign, data)

向服务器发送一条消息

**参数：**

* sign：请求标识符，类型为**string**，由为三位大写的字母构成，用于服务器识别此消息的类型。若值为**None**，则不发送请求标识符。

* data：发送的消息，类型为**string**。若值为**None**，则不发送消息

**返回值：**

* True：消息发送成功
* False：消息发送失败

---

### TcpCliSock.recvstr()

从服务器接收一条字符串

**返回值：** 接收的消息，类型为 **string**

---

### TcpCliSock.recvbyte()

从服务器接收一条byte串

**返回值：** 接收的消息，类型为 **bytes**

---

### TcpCliSock.close()

关闭客户端套接字



## pyDes.py

由**MIT**开发，**DES**加密算法的python实现，支持**3DES**

> DES全称为Data Encryption Standard，即数据加密标准，是一种使用[密钥加密](https://baike.baidu.com/item/密钥加密/5928903)的块算法，1977年被[美国联邦政府](https://baike.baidu.com/item/美国联邦政府/8370227)的国家标准局确定为[联邦资料处理标准](https://baike.baidu.com/item/联邦资料处理标准/3940777)（FIPS），并授权在非密级政府通信中使用，随后该算法在国际上广泛流传开来。需要注意的是，在某些文献中，作为算法的DES称为数据加密算法（Data Encryption Algorithm,DEA），已与作为标准的DES区分开来。

为方便调用，适合本通信系统的加密函数在**crypto.py**中实现



## crypto.py

密码学工具包，包含：**对称密码、散列函数、快速密钥交换**

> ##### 对称加密算法
>
> 对称加密算法是应用较早的加密算法，技术成熟。在对称加密算法中，数据发信方将明文（原始数据）和加密密钥一起经过特殊加密算法处理后，使其变成复杂的加密密文发送出去。收信方收到密文后，若想解读原文，则需要使用加密用过的密钥及相同算法的逆算法对密文进行解密，才能使其恢复成可读明文。在对称加密算法中，使用的密钥只有一个，发收信双方都使用这个密钥对数据进行加密和解密，这就要求解密方事先必须知道加密密钥。
>
> ##### 单项散列函数
>
> 单向[散列函数](https://baike.baidu.com/item/散列函数)，又称单向[Hash函数](https://baike.baidu.com/item/Hash函数)、杂凑函数，就是把任意长的输入消息串变化成固定长的输出串且由输出串难以得到输入串的一种函数。这个输出串称为该消息的散列值。一般用于产生[消息摘要](https://baike.baidu.com/item/消息摘要/4547744)，[密钥](https://baike.baidu.com/item/密钥)加密等.
>
> ##### 快速秘钥交换
>
> 以公钥密码加密对称密码的密钥从而解决密钥分发问题的混合加密系统使用广泛，而 Diffie-Hellman 交换方法由于交换密钥需要多次通信，很少应用于邮件等离线通信情景。快速密钥交换（Fast Key Exchange）是一种离线的快速的密钥交换协议，可以达到一次单向通信即可完成密钥协定与密文传送。本协议是Chen_Py原创（至少截止2020年2月没看到别人用过）

---

### encrypt(data, key, iv)

字符串加密函数

**参数：**

* data： 待加密的字符串（明文），类型为**string**
* key：密钥，类型为**int**
* iv：初始向量，类型为**int**

**返回值：** 加密的结果（密文），类型为**bytes**

---

### decrypt(data, key, iv)

密文解密函数

**参数：**

* data：待解密的密文，类型为**bytes**
* key：密钥，类型为**int**
* iv：初始向量，类型为**int**

**返回值：** 解密的结果（明文），类型为**string**

---

### hash(data)

单向散列函数

**参数：**

* data：待哈希的字符串，类型为**string**

**返回值：** 散列函数的结果（哈希值），类型为**int**

---

### Make_Private_Code(N, m, Private_Secret_Code)

计算**FKE**中的个人码（*Private Code*）

**参数：**

* N：个人明码构成要素之一，类型为**int**，最大为**24byte**
* m：个人明码构成要素之一，类型为**int**，最大为**24byte**
* Private_Secret_Code：个人暗码，类型为**int**，最大为**24byte**

**返回值：** 元组：**(Private_Open_Code, Private_Secret_Code)**

* Private_Open_Code：个人明码，类型为**tuple**，格式为(N, m, P)
* Private_Secret_Code：个人暗码，类型为**int**

---

### Make_Communication_Code(Private_Open_Code, Communication_secret_Code)

计算**FKE**中的通信码（*Communication Code*）和密钥（*Key*）

**参数：**

* Private_Open_Code：收件人的个人明码，类型为**tuple**，格式为(N,m,P)
* Communication_secret_Code：通信暗码，类型为**int**，最大为**24byte**

**返回值：** 元组：**(Communication_Open_Code, Communication_Secret_Code, Key)**

* Communication_Open_Code：通信明码，类型为**int**
* Communication_Secret_Code：通信暗码，类型为**int**
* Key：通信密钥，类型为**int**

---

### Make_Key(Communication_Open_Code, m, Private_Secret_Code)

计算通信密钥（*Key*）

**参数：**

* Communication_Open_Code：通信明码，类型为**int**

* m：个人明码(N, m, P)中的m，类型为**int**
* Private_Secret_Code：个人暗码，类型为**int**

**返回值：** 通信密钥**Key**，类型为**int**



## serverbase.py

服务器基本框架，为每一个连接的客户端创建线程分别提供服务

### ServerBase

面向单个客户端的服务类

**构造函数：** *ServerBase(clisock, ip)*

---

#### # server methods

此处实现服务器的各种功能

---

#### run()

线程主函数，主要任务是读取请求标识符并执行相应的操作，并在客户端异常退出时结束该线程