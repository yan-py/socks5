import socket
from socks_lib import SocksLib as socks
import sys

a = socks('127.1', 1080)
socket = a.connect('google.com', 80)

socket.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')
data = socket.recv(4096)
if data:
    print(data.decode())
