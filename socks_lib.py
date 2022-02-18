import socket
import struct
import sys

class SocksLib:

    def __init__(self, socks_ip, socks_port):
        self.socks_ver = 5
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socks_ip, int(socks_port))
    
    def auth(self, login, password):
        self.sock.connect(self.server_address)
        auth_msg = struct.pack('!BBBB', self.socks_ver, 2, 0, 2)
        self.sock.send(auth_msg)
        answ = self.sock.recv(2)
        
        auth_msg = struct.pack("!BB", 1, len(login)) + login.encode() + struct.pack("!B", len(password)) + password.encode()
        self.sock.send(auth_msg)
        answ = self.sock.recv(2)

    def connect(self, address, port, login, password):
        self.auth(login, password)
        try:
            self.target_addr = socket.inet_aton(address)
            self.address_type = struct.pack('!B', 1)
        except socket.error:
            self.target_addr = address.encode()
            self.address_type = struct.pack("!BB", 3, len(address))
        self.target_port = struct.pack('!H', port)
        
        request = struct.pack('!BBB', self.socks_ver, 1, 0) + self.address_type + self.target_addr + self.target_port
        self.sock.send(request)
        answ = self.sock.recv(64)

        return self.sock
