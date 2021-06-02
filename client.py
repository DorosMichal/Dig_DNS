import socket
import select
from time import time
import dns.message as mes

class Client:
    DNS_PORT = 53
    TIMEOUT = 0.5
    MAX_TRIES = 3
    MAX_UDP = 2**16
    def __init__(self, protocol):
        self.protocol = protocol
        self.sock = Client._create_socket(protocol)

    def __del__(self):
        self.sock.close()
    
    @staticmethod
    def _create_socket(protocol):
        try:
            type = socket.SOCK_DGRAM if protocol == "UDP" else socket.SOCK_STREAM
            return socket.socket(socket.AF_INET, type)
        except socket.error as e:
            print(f"error, creating socket failed: {e}")
            exit(1)


    def _send_query_udp(self, message, server_ip):
        addr = (server_ip, Client.DNS_PORT)
        try:
            self.sock.sendto(message.to_wire(), addr)
        except socket.error as e:
            print(f"error, socket sendto failed: {e}")
            self.__del__()
            exit(1)


    def _recive_response(self, server_ip):
        timeout = Client.TIMEOUT
        stop_time = time() + Client.TIMEOUT
        while True:
            ready, _, _ = select.select([self.sock], [], [], timeout) #error handling
            if ready:
                resp, addr = self.sock.recvfrom(Client.MAX_UDP)
                ip, port = addr
                if ip != server_ip or port != Client.DNS_PORT:
                    timeout = max(0, stop_time - time())
                    continue
                return mes.from_wire(resp) #error handling
            return None

    def run_query(self, message, server_ip):
        if self.protocol == "UDP":
            tries = 0
            while tries < Client.MAX_TRIES:
                self._send_query_udp(message, server_ip)
                response = self._recive_response(server_ip)
                if response:
                    return response
                else:
                    tries += 1

        #if udp didnt work or tcp was chosen
        # if self.protocol == "UDP":
        #     self.sock.close()
        #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # addr = (server_ip, Client.DNS_PORT)
        # try:
        #     self.sock.connect(addr)
        #     _send_query_tcp(domain_name, server_ip, query_type)
        # except socket.error as e:
        #   ...