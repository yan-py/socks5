import socket
import sys

class SocksLib:

    def __init__(self, socks_ip, socks_port):
        self.socks_ver = '\x05'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socks_ip, int(socks_port))
    
    def auth(self):
        self.sock.connect(self.server_address)
        auth_msg = f'{self.socks_ver}\x01\x00'
        self.sock.send(auth_msg.encode())
        answ = self.sock.recv(2)

    def request(self, address, port):
        try:
            self.target_addr = socket.inet_aton(address)
            self.address_type = '\x01'
        except socket.error:
            self.target_addr = address.encode()
            self.address_type = '\x03' + chr(len(address))
        self.target_port = chr(0)+chr(port)

        request = f'{self.socks_ver}\x01\x00{self.address_type}'.encode() + self.target_addr + self.target_port.encode()
        self.sock.send(request)
        answ = self.sock.recv(128)
        return self.sock
