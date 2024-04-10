# Tx 

# socket comm # AWR1843.cfg file to board 

import socket
import serial
import time
import numpy as np

def send_data(ip, port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((ip, port))
        client_socket.sendall(data.encode())
        print("send data : ", data) 
        
    finally:
        client_socket.close()

def serialConfig(configFileName):
    
    global CLIport
    global Dataport

    CLIport = serial.Serial('COM10', 115200)
    Dataport = serial.Serial('COM9', 921600)

    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        CLIport.write((i+'\n').encode())
        print(i)
        time.sleep(0.01)
        
    config_data = '\n'.join(config) 
    server_ip = '192.168.33.30'  
    server_port = 4098  
    send_data(server_ip, server_port, config_data)
    
    return CLIport, Dataport

def parseConfigFile(configFileName):
    configParameters = {} 
    
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        
        splitWords = i.split(" ")
        
        numRxAnt = 4
        numTxAnt = 3
        
        if "profileCfg" in splitWords[0]:
            startFreq = int(float(splitWords[2]))
            idleTime = int(splitWords[3])
            rampEndTime = float(splitWords[5])
            freqSlopeConst = float(splitWords[8])
            numAdcSamples = int(splitWords[10])
            numAdcSamplesRoundTo2 = 1;
            
            while numAdcSamples > numAdcSamplesRoundTo2:
                numAdcSamplesRoundTo2 = numAdcSamplesRoundTo2 * 2;
                
            digOutSampleRate = int(splitWords[11]);
            
        elif "frameCfg" in splitWords[0]:
            
            chirpStartIdx = int(splitWords[1]);
            chirpEndIdx = int(splitWords[2]);
            numLoops = int(splitWords[3]);
            numFrames = int(splitWords[4]);
            framePeriodicity = float(splitWords[5]);

              
    numChirpsPerFrame = (chirpEndIdx - chirpStartIdx + 1) * numLoops
    configParameters["numDopplerBins"] = numChirpsPerFrame / numTxAnt
    configParameters["numRangeBins"] = numAdcSamplesRoundTo2
    configParameters["rangeResolutionMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * numAdcSamples)
    configParameters["rangeIdxToMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * configParameters["numRangeBins"])
    configParameters["dopplerResolutionMps"] = 3e8 / (2 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * configParameters["numDopplerBins"] * numTxAnt)
    configParameters["maxRange"] = (300 * 0.9 * digOutSampleRate)/(2 * freqSlopeConst * 1e3)
    configParameters["maxVelocity"] = 3e8 / (4 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * numTxAnt)
    
    return configParameters

if __name__ == "__main__":
    configFileName = 'AWR1843config.cfg'
    CLIport, Dataport = serialConfig(configFileName)
    configParams = parseConfigFile(configFileName)
