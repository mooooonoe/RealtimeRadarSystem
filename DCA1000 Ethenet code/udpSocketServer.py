import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))

print("UDP Echo Server is running...")

while True:
    # Receive message from client
    data, addr = server_socket.recvfrom(1024)
    print("Received message from:", addr)
    print("Message:", data.decode())

    # Check for exit command
    if data.decode().strip().lower() == "q":
        print("Server is shutting down...")
        break

    # Echo back the received message
    server_socket.sendto(data, addr)  # Echo back to the client

    # Receive message from server
    server_response = input("Enter message to send back to client (press Enter to skip):")
    if server_response:  # If server_response is not empty
        server_socket.sendto(server_response.encode(), addr)

server_socket.close()
