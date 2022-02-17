import socket
import sys

# init
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (sys.argv[1], int(sys.argv[2]))
sock.connect(server_address)
try:
    req_addr = socket.inet_aton(sys.argv[3])
    address_type = '\x01'
except socket.error:
    req_addr = sys.argv[3].encode()
    address_type = '\x03'+chr(len(sys.argv[3]))

# request auth
msg = '\x05\x02\x00\x02'
sock.send(msg.encode())
answ = sock.recv(2)

# request connect
request = '\x05\x01\x00'.encode()+address_type.encode()+req_addr+'\x00P'.encode()# 80 port
sock.send(request)
answ = sock.recv(16)

# request page
sock.send(b'GET / HTTP/1.1\r\nHost: '+req_addr+b'\r\n\r\n')

data = sock.recv(4096)
if data:
    print(data.decode())
