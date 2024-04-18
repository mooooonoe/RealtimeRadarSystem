import socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Send message to server
    msg = input("Enter message to send (press Enter to skip):")
    if msg == 'q':
        client_socket.sendto(msg.encode(), ('localhost', 12345))
        break
    elif msg:  # If msg is not empty
        client_socket.sendto(msg.encode(), ('localhost', 12345))

    # Receive message from server
    data, addr = client_socket.recvfrom(1024)
    print('Received from server:', data.decode())

client_socket.close()
