# Rx

import socket

def receive_data(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.33.30', port))
    server_socket.listen(1)
    print("waiting...")
    connection, client_address = server_socket.accept()
    try:
        print("binding:", client_address)
        data = connection.recv(1024).decode()
        print("received DATA : ", data)
        
    finally:
        connection.close()
        server_socket.close()

receive_port = 4098

receive_data(receive_port)
