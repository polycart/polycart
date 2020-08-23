from clientbase.clientbase import ClientBase
client = ClientBase()
print(client.clisock.state)
print(client.RequestMmanualIntervention((3,3)))