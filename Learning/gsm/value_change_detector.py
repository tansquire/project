#!/usr/bin/python
import time
import mysql.connector
new_stuf_club_value=new_childrenpark_value=new_lakewell_value=new_RR_sump_value=new_actuator_value=old_stuf_club_value=old_childrenpark_value=old_lakewell_value=old_RR_sump_value=old_actuator_value=0
stuff_club_comm_status=childrenpark_comm_status=lakewell_comm_status=RR_sump_comm_status=actuator_comm_status=0

def getvalue(i):
 conn=mysql.connector.connect(user='root',password='gowsalya',host='10.21.160.201',database='scada')
 mycursor=conn.cursor()
 mycursor.execute("select * FROM AI where id=%s",(i,)) 
 list=mycursor.fetchall()
 return (list[0][2])
 conn.close()
 mycursor.close()

while(1):

 new_stuf_club_value=getvalue(7)
 new_childrenpark_value=getvalue(6)
 new_lakewell_value=getvalue(5)
 new_RR_sump_value=getvalue(8)
 new_actuator_value=getvalue(9)
 
 if (new_stuf_club_value != old_stuf_club_value):
  stuff_club_comm_status=1
  old_stuf_club_value = new_stuf_club_value
 else:
  stuff_club_comm_status=0
 
 if (new_childrenpark_value != old_childrenpark_value):
  childrenpark_comm_status=1
  old_childrenpark_value = new_childrenpark_value
 else:
  childrenpark_comm_status=0

 if (new_lakewell_value != old_lakewell_value):
  lakewell_comm_status=1
  old_lakewell_value = new_lakewell_value
 else:
  lakewell_comm_status=0

 if (new_RR_sump_value != old_RR_sump_value):
  RR_sump_comm_status=1
  old_RR_sump_value = new_RR_sump_value
 else:
  RR_sump_comm_status=0

 if (new_actuator_value != old_actuator_value):
  actuator_comm_status=1
  old_actuator_value = new_actuator_value
 else:
  actuator_comm_status=0
 
 conn=mysql.connector.connect(user='root',password='gowsalya',host='10.21.160.201',database='scada')
 mycursor=conn.cursor()
 mycursor.execute("UPDATE DI SET value='%s'WHERE id='%s'" % (lakewell_comm_status, 3))
 mycursor.execute("UPDATE DI SET value='%s'WHERE id='%s'" % (childrenpark_comm_status, 4))
 mycursor.execute("UPDATE DI SET value='%s'WHERE id='%s'" % (stuff_club_comm_status, 5))
 mycursor.execute("UPDATE DI SET value='%s'WHERE id='%s'" % (RR_sump_comm_status, 6))
 mycursor.execute("UPDATE DI SET value='%s'WHERE id='%s'" % (actuator_comm_status, 7))
 print"lakewell, children, stuff_club, RR sump, actuator comm availabilities respectively are=%s, %s, %s, %s and %s"%(lakewell_comm_status,childrenpark_comm_status,stuff_club_comm_status, RR_sump_comm_status, actuator_comm_status)
 conn.commit()
 conn.close()
 mycursor.close()
 time.sleep(3)   
#this time must be greater than gate random update time(so gateway freq must be known)
