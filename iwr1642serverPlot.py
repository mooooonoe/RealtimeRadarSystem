import socket
import threading
import time
import os
from queue import Queue
import json
import numpy as np
import matplotlib.pyplot as plt

from func_plot import update_plot, process_plot_queue

clients = []
command_queue = Queue()
plot_queue = Queue()


def json_to_numpy(data):
    """ JSON 데이터를 numpy 배열로 변환 """
    for key, value in data.items():
        if isinstance(value, list):
            try:
                data[key] = np.array(value, dtype=np.int64)
            except ValueError:
                pass
    return data


def handle_client(client_socket):
    client_socket.send("hi im server".encode())  # Initial message to the client
    partial_data = ""
    
    while True:
        try:
            data = client_socket.recv(65535)
            if not data:
                break
            partial_data += data.decode('utf-8')

            # 데이터가 완전한 JSON 형식인지 확인
            try:
                received_data = json.loads(partial_data)
                
                # JSON 데이터를 numpy 배열로 변환
                received_data = json_to_numpy(received_data)
                frameNumber = received_data['frameNumber']
                currChDataI = received_data['currChDataI']
                currChDataQ = received_data['currChDataQ']
                rangeArray = received_data['rangeArray']
                dopplerArray = received_data['dopplerArray']
                rangeDoppler = received_data['rangeDoppler']

                rangeArray = np.array(rangeArray, dtype=np.int16)
                dopplerArray = np.array(dopplerArray, dtype=np.int16)
                rangeDoppler = np.array(rangeDoppler, dtype=np.int16)

                print('수신된 데이터:')
                print('frameNumber:', frameNumber)
                print('currChDataI:', currChDataI)
                print('currChDataQ:', currChDataQ)
                print('rangeArray:', rangeArray)
                print('dopplerArray:', dopplerArray)
                print('rangeDoppler:', rangeDoppler)

                print("\nshape:", rangeDoppler.shape)
                print("\nsize:", rangeDoppler.size)
                print("\ndtype:", rangeDoppler.dtype)

                update_plot(currChDataI, currChDataQ, rangeArray,dopplerArray,rangeDoppler)
                # 처리 후 partial_data 초기화
                partial_data = ""

            except json.JSONDecodeError:
                # JSON 데이터가 완전하지 않은 경우, 계속 수신
                continue
        except Exception as e:
            print(f"Error in handle_client: {e}")
            break
    client_socket.close()

def server_loop(server_socket):
    while True:
        try:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except OSError:
            break  # This will break the loop if server_socket is closed

def handle_commands():
    while True:
        command = command_queue.get()
        if command:
            print(f"Sending command to clients: {command}")
            for client in clients:
                try:
                    client.send(command.encode())
                except:
                    pass

def shutdown_server(server_socket):
    print("Server is shutting down. Notifying clients...")
    for client in clients:
        try:
            client.send("sensorStop".encode())
            time.sleep(3)
            client.close()
        except:
            pass
    try:
        server_socket.close()
    except:
        pass
    print("Server has shut down.")
    os._exit(0)

def server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server listening on port 12345")

    server_thread = threading.Thread(target=server_loop, args=(server_socket,))
    server_thread.start()

    command_thread = threading.Thread(target=handle_commands)
    command_thread.start()

    try:
        while True:
            process_plot_queue() # 주기적으로 큐를 확인하고, 플롯을 업데이트함
            time.sleep(0.01)
            command = input()
            command_queue.put(command)
    except KeyboardInterrupt:
        shutdown_server(server_socket)

if __name__ == "__main__":
    server()
