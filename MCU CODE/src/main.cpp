#include <Arduino.h>

//libraries included
#include <EEPROM.h>  
#include <SoftwareSerial.h>

//constant declarations  
#define MaxLength 1000
int address = 0;
bool calltransmit = false;
bool callRecieve = true;
bool exitvoidloop = false;
int ptr = 0;
int max_ptr = 0;

//private function declarations
void EEPROMClear();   
void ReceiveAndStoreData();
void TransmitDataWithSpeedMeasurement(int pointer);

//code to run only once
void setup() {  
  Serial.begin(2400); 
  delay(100); 
  EEPROMClear();
}

//code on loop
void loop() {
  if(exitvoidloop){
    return;
  }
  ReceiveAndStoreData(); 
  TransmitDataWithSpeedMeasurement(0);
}

//Function to empty all previous values writen in EEPROM or NVS
void EEPROMClear(){
  while(Serial.available()>0){
    byte data = Serial.read();
    if(data == '1'){
      for (int i = 0 ; i < EEPROM.length() ; i++) {
      EEPROM.write(i, 0);
      }
      break;
    }
  } 
  Serial.println("EEPROM emptied, and is ready to store new data!!");
}

//Function to recieve and store data in EEPROM
void ReceiveAndStoreData() {

  if(!callRecieve){
    return;
  }

  while (Serial.available()>0) { 

    if (address < MaxLength) {
      byte data = Serial.read();
      if (data == 36){
        calltransmit = true;
        return;
      }
      EEPROM.write(address, data);
      address++;
      delay(416);     //wait to read the next character on serial ~ 1/2400 since selected baud rate is 2400
    } else {
      Serial.println("Buffer overflow!");
      delay(2000);
      return;
    }
    Serial.write("Start Sending again");
  }
}

//Function to transmit data after extracting it from storage
void TransmitDataWithSpeedMeasurement(int pointer) {
  if(!calltransmit){
    ReceiveAndStoreData();
    return;
  }
  ptr = pointer;
  max_ptr = ptr+64;

  for(ptr ; ptr < max_ptr; ptr++){
    char data = EEPROM.read(ptr);
    if(data == '\0'){
      Serial.write("$");
      exitvoidloop = true;
      return;
    }
    Serial.write(data); 
  }

  delay(100);
  TransmitDataWithSpeedMeasurement(max_ptr);

  callRecieve = false;
}