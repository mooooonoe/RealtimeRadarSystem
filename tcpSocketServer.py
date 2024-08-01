# server -> 아니ㅁ 이게 client 가 Tx 임 

# 가장 먼저 시리얼로 cfg 파일을 넣어준다

# 그러면 시리얼로 데이터가 들어오고 있는지 확인

# socket 통신으로 일단 client 랑 binding 
# data 시작 찾기

#serial import

import serial 
import numpy as np

# socket import
import socket

# serial main
comport = input("mmWave:Auxillary Data port (Demo output DATA_port) =")
ser = serial.Serial(comport, 921600)

ser.isOpen()


while True:
    byteCount = ser.inWaiting()
    byte_str = ser.read(byteCount)

    if not byte_str:
        continue

    byte_str(byte_str)

    msg = input()
    if msg == 'q':
        comport.close()
        break

# socket main
def send_data(ip, port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        client_socket.conect((ip,port))
        client_socket.sendall(data.encode())

    finally:
        client_socket.close()

# server ? client ?
server_ip = '192.168.33.30'
server_port = 4098

test_data = "Hello Radar ! Ready to read the cfg file?"

send_data(server_ip, server_port, test_data)