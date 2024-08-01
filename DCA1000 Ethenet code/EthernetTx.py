# Tx # client

import socket

def send_data(ip, port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((ip, port))
        client_socket.sendall(data.encode())
        print("send data : ", data) 
        
    finally:
        client_socket.close()
test_data = "Hello, Server!"

server_ip = '192.168.33.30'
server_port = 4098

send_data(server_ip, server_port, test_data)
