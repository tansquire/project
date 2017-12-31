#include <RadioHead.h>
#include <RHGenericSPI.h>
#include <RH_NRF51.h>
#include <RHCRC.h>
#include <RHRouter.h>
#include <RH_RF95.h>
#include <RHSoftwareSPI.h>
#include <RHDatagram.h>
#include <RH_CC110.h>
#include <RH_E32.h>
#include <RHHardwareSPI.h>
#include <RH_RF24.h>
#include <RH_RF22.h>
#include <RHSPIDriver.h>
#include <RH_MRF89.h>
#include <RHEncryptedDriver.h>
#include <RHGenericDriver.h>
#include <RH_NRF24.h>
#include <RHReliableDatagram.h>
#include <RHTcpProtocol.h>
#include <RH_Serial.h>
#include <RH_ASK.h>
#include <RHNRFSPIDriver.h>
#include <RH_TCP.h>
#include <RH_RF69.h>
#include <RHMesh.h>
#include <RH_NRF905.h>

/*
  LoRa Simple Client for Arduino :
  Support Devices: LoRa Shield + Arduino 
  
  Example sketch showing how to create a simple messageing client, 
  with the RH_RF95 class. RH_RF95 class does not provide for addressing or
  reliability, so you should only use RH_RF95 if you do not need the higher
  level messaging abilities.

  It is designed to work with the other example LoRa Simple Server

  modified 16 11 2016
  by Edwin Chen <support@dragino.com>
  Dragino Technology Co., Limited
*/

#include <SPI.h>
#include <RH_RF95.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
float frequency = 868.0;
int open = 8;
int close = 9;
int opened = 4;
int remote = 3;
int closed = 5;
int x;


void setup() 
{
  pinMode(open, OUTPUT); 
   pinMode(close, OUTPUT); 
   pinMode(opened, INPUT);
    pinMode(remote, INPUT);
    pinMode(closed, INPUT);
  Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  Serial.println("Start LoRa Client");
  if (!rf95.init())
    Serial.println("init failed");
  // Setup ISM frequency
  rf95.setFrequency(frequency);
  // Setup Power,dBm
  rf95.setTxPower(13);
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
}

void loop()
{


  Serial.println("Sending to LoRa Server");
  // Send a message to LoRa Server
  uint8_t data[4];
  data[0]=9;

  if(digitalRead(remote))
  data[1]=7;
  else 
  data[1]=6;


  if(digitalRead(opened))
  data[2]=7;
  else 
  data[2]=6;

  if(digitalRead(closed))
  data[3]=7;
  else 
  data[3]=6;
      

  //data[3]=digitalRead(closed);
  //delay(1);      

  
  rf95.send(data, sizeof(data));
  
  rf95.waitPacketSent();
  // Now wait for a reply
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (rf95.waitAvailableTimeout(3000))
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, &len))
   {
      Serial.println("got reply");

//Serial.println((char*)buf);
     Serial.print(*buf);
      Serial.print(*(buf+1));
     Serial.println(*(buf+2));


x= *(buf+1);

 if(!digitalRead(opened) && digitalRead(remote))
  {
  if(x==1)
 {
  digitalWrite(close, LOW);
  delay(5);
  digitalWrite(open, HIGH);
  x=0;

}
  }
else
digitalWrite(open, LOW);



 if(!digitalRead(closed) && digitalRead(remote))
  {
  if(x==2)
 {
   digitalWrite(open, LOW);
   delay(5);
   digitalWrite(close, HIGH);
   x=0;

}
  }
else
digitalWrite(close, LOW);



 
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC); 

     
    }
    else
    {
      Serial.println("recv failed");
    }
  }
  else
  {
    Serial.println("No reply, is LoRa server running?");
  }
  delay(7000);
}


