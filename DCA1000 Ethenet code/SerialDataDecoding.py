import serial
import numpy as np
import struct

comport = input("mmWave:Auxillary Data port (Demo output DATA_port) = ")

ser = serial.Serial(comport, 921600)

ser.isOpen()

magicWord = [2, 1, 4, 3, 6, 5, 8, 7]

with open("data_file.txt", "w") as file:

    def parseData(byteBuffer):

        MMWDEMO_UART_MSG_DETECTED_POINTS = 1
        # MMWDEMO_UART_MSG_RANGE_PROFILE   = 2
        # MMWDEMO_OUTPUT_MSG_NOISE_PROFILE = 3
        # MMWDEMO_OUTPUT_MSG_AZIMUT_STATIC_HEAT_MAP = 4
        # MMWDEMO_OUTPUT_MSG_RANGE_DOPPLER_HEAT_MAP = 5

        idX = 0
        # Read the header
        magicNumber = byteBuffer[idX:idX+8]
        idX += 8
        version = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        totalPacketLen = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        platform = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        frameNumber = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        timeCpuCycles = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        numDetectedObj = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        numTLVs = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4
        subFrameNumber = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
        idX += 4

        # Read the TLV messages
        for tlvIdx in range(numTLVs):
            tlv_type = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
            idX += 4
            tlv_length = struct.unpack('<I', bytes(byteBuffer[idX:idX+4]))[0]
            idX += 4
            
            print("TLV Type:", tlv_type)
            print("TLV Length:", tlv_length)

            if tlv_type == MMWDEMO_UART_MSG_DETECTED_POINTS:

                x = np.zeros(numDetectedObj,dtype=np.float32)
                y = np.zeros(numDetectedObj,dtype=np.float32)
                z = np.zeros(numDetectedObj,dtype=np.float32)
                velocity = np.zeros(numDetectedObj,dtype=np.float32)
                    
                for objectNum in range(numDetectedObj):
                    
                    x_bytes = byteBuffer[idX:idX + 4] 
                    x_float = struct.unpack('<f', x_bytes)[0] 
                    x[objectNum] = round(x_float, 3)
                    idX += 4 

                    y_bytes = byteBuffer[idX:idX + 4]
                    y_float = struct.unpack('<f', y_bytes)[0]
                    y[objectNum] = round(y_float, 3)
                    idX += 4

                    z_bytes = byteBuffer[idX:idX + 4]
                    z_float = struct.unpack('<f', z_bytes)[0]
                    z[objectNum] = round(z_float, 3)
                    idX += 4

                    velocity_bytes = byteBuffer[idX:idX + 4]
                    velocity_float = struct.unpack('<f', velocity_bytes)[0]
                    velocity[objectNum] = round(velocity_float, 3)
                    idX += 4
                
                detObj = {"numObj": numDetectedObj, "x": x, "y": y, "z": z, "velocity":velocity}
                print("Frame Number:", frameNumber)
                print("numObj:", numDetectedObj, "x:", x, "y:", y, "z:", z, "velocity:", velocity)

                file.write(f"Frame Number: {frameNumber}\tdetObj: {numDetectedObj}\n")

                for obj_num in range(numDetectedObj):
                    file.write(f"\t{round(x[obj_num], 3)}\t\t{round(y[obj_num], 3)}\t\t{round(velocity[obj_num], 3)}\n")

    # ---- ---- ---- ---- ---- ---- ---- ---- MAIN ---- ---- ---- ---- ---- ---- ---- ----
    
    while True:
        byteCount = ser.inWaiting()
        byte_str = ser.read(byteCount)
        
        if not byte_str:
            continue
        
        start_index = byte_str.find(bytes(magicWord))
        
        if start_index == -1:
            continue
        
        packet_data = byte_str[start_index:]
    
        parseData(byte_str)
