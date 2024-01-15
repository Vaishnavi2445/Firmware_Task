import serial
import time

arduino = serial.Serial(port='COM3', baudrate=2400)

time.sleep(1)

message = """Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one.

In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently."""
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
