#!/usr/bin/python
import serial
import time
import mysql.connector

ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

def getvalue():
 ser.write(b'g')
 data=ser.readline().decode('ascii')
 data=str(data)
 return data

def opened():
 ser.write(b'c')
 data=ser.readline()
 data=str(data)
 return data

def remote():
 ser.write(b'd')
 data=ser.readline()
 data=str(data)
 return data

def closed():
 ser.write(b'e')
 data=ser.readline()
 data=str(data)
 return data



def open():
 conn=mysql.connector.connect(user='root',password='gowsalya',host='10.21.160.201',database='test')
 mycursor=conn.cursor()
 ser.write(b'a')
 mycursor.execute("UPDATE command SET open= '0' WHERE valve=1")
 conn.commit()
 conn.close()
 mycursor.close()
 return

def close():
 conn=mysql.connector.connect(user='root',password='gowsalya',host='10.21.160.201',database='test')
 mycursor=conn.cursor()
 ser.write(b'b')
 mycursor.execute("UPDATE command SET close= '0' WHERE valve=1")
 conn.commit()
 conn.close()
 mycursor.close()
 return


while(1):
 conn=mysql.connector.connect(user='root',password='gowsalya',host='10.21.160.201',database='test')
 mycursor=conn.cursor()
 mycursor.execute('select * FROM command') 
 list=mycursor.fetchall()
 print(list[0][2])
 print(list[0][1])
 
 time.sleep(2)
 if(list[0][1]=='1'):
  open()
 if(list[0][2]=='1'):
   close()
  
 mycursor.execute("UPDATE command SET opened= %s WHERE valve=1" %(opened()))
 mycursor.execute("UPDATE command SET closed= %s WHERE valve=1" %(closed()))
 #mycursor.execute("UPDATE command SET remote= %s WHERE valve=1" %(remote()))
 mycursor.execute("UPDATE command SET remote= '1' WHERE valve=1")
 conn.commit()
 conn.close()
 mycursor.close()
 time.sleep(1)


