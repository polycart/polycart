from clientbase.clientbase import ClientBase
client = ClientBase()
print(client.clisock.state)
reslist = client.SearchForGoods("Chen")
print(reslist[0])