import socket as s
import sys
from dnslib import DNSRecord,RR,QTYPE,RCODE,parse_time
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger



IP = "127.0.0.1"
PORT = 1234
IP_PORT = (IP, PORT)


# #Creation of socket (INET = IPV4, SOCKET_STREAM = type(TCP))
# client = s.socket(s.AF_INET,
#                   s.SOCK_STREAM)
# print("[Client] Socket Created")

# #Socket Connection
# try:
#     client.connect(IP_PORT)
#     print(f"[Client] Socket connected to host: {str(IP_PORT)}")
# except s.error as e:
#     print(e)
#     sys.exit()

q = DNSRecord.question("www.baidu.com")
a = q.send(IP,PORT)


# #Socket Receive / Send
# try:
#     print(client.recv(100).decode())
# except s.error as e:
#     print(e)
#     sys.exit()

# client.close()
print(DNSRecord.parse(a))
