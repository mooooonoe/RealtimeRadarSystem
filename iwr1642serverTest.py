import socket
import threading
import time
import os
from queue import Queue
import json
import numpy as np
import matplotlib.pyplot as plt

clients = []
command_queue = Queue()
plot_queue = Queue()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

line1, = ax1.plot([], [], label='I Channel')
line2, = ax1.plot([], [], label='Q Channel')
ax1.set_xlabel('time (samples)')
ax1.set_ylabel('ADC time domain output')
ax1.set_title('Time Domain Output')
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Doppler(m/s)')
ax2.set_ylabel('Range(meters)')
ax2.set_title('Range Doppler Output')
ax2.grid(True)

def update_rangeprofile_plot(I_data, Q_data):
    line1.set_ydata(I_data)
    line2.set_ydata(Q_data)
    line1.set_xdata(np.arange(len(I_data)))
    line2.set_xdata(np.arange(len(Q_data)))
    ax1.relim()
    ax1.autoscale_view()

def update_rangedoppler_plot(rangeArray, dopplerArray, rangeDoppler):
    ax2.cla()
    ax2.contourf(rangeArray, dopplerArray, rangeDoppler, cmap='jet')
    ax2.grid(True)

def json_to_numpy(data):
    """ JSON 데이터를 numpy 배열로 변환 """
    for key, value in data.items():
        if isinstance(value, list):
            try:
                data[key] = np.array(value, dtype=np.int16)
            except ValueError:
                pass
    rangeDoppler = data['rangeDoppler']
    print("\n rangedoppler: ", rangeDoppler)
    print("\nshape:", rangeDoppler.shape)
    print("\nsize:", rangeDoppler.size)
    print("\ndtype:", rangeDoppler.dtype)

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

                print('수신된 데이터:')
                print('frameNumber:', frameNumber)
                
                plot_queue.put((currChDataI, currChDataQ, rangeArray, dopplerArray, rangeDoppler))

                # 처리 후 partial_data 초기화
                partial_data = ""

            except json.JSONDecodeError:
                # JSON 데이터가 완전하지 않은 경우, 계속 수신
                continue
        except Exception as e:
            print(f"Error in handle_client: {e}")
            break
    client_socket.close()

def plot_update_loop():
    plt.ion()  # Interactive mode on
    while True:
        data = plot_queue.get()
        if data:
            currChDataI, currChDataQ, rangeArray, dopplerArray, rangeDoppler = data
            update_rangeprofile_plot(currChDataI, currChDataQ)
            update_rangedoppler_plot(rangeArray, dopplerArray, rangeDoppler)
            plt.draw()
            plt.pause(0.01)

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

def command_input_thread():
    while True:
        command = input()
        command_queue.put(command)

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

    plot_thread = threading.Thread(target=plot_update_loop)
    plot_thread.start()

    try:
        while True:
            command = input()
            command_queue.put(command)
    except KeyboardInterrupt:
        shutdown_server(server_socket)

if __name__ == "__main__":
    server()
