import serial
import time

arduino = serial.Serial(port='COM3', baudrate=2400)

time.sleep(1)

message = """Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan ..."""

while True:
    response = arduino.readline().decode('utf-8').strip()
    if response == "EEPROM emptied, and is ready to store new data!!":
        break
    else:
        print("Waiting for EEPROM to be cleared...")
        time.sleep(1)

def Senddata(data):
    arduino.write(data.encode('UTF-8'))

def sendData():
    i = 0
    while i < len(message):
        Senddata(message[i:i+64])
        i += 64

        while True:
            new_response = arduino.readline().decode('utf-8').strip()
            print("Received:", new_response)
            if new_response == "Start Sending again":
                break
            elif new_response == "Buffer overflow!":
                print("Buffer overflow!")
                return
            else:
                print("Unexpected response:", new_response)
                return

    new_data = "$"
    Senddata(new_data)

def receiveData():
    while True:
        new_response = arduino.readline().decode('utf-8').strip()
        print("Received:", new_response)
        if new_response == "$":
            break

sendData()
receiveData()

arduino.close()
