'''
Created on Apr 16, 2015

@author: pdesai
'''
import pyLIN
import time

ACTIVE_MODE_SLEEP = 0.001
SLAVE_ADDRESS = 0xC4

DIAGNOSTIC_MSG = {"TPM_ID_0":"60 02 22 20 FF FF FF FF 5B",                  
                  "TPM_ID_1":"60 02 22 21 FF FF FF FF 5A",
                  "TPM_ID_2":"60 02 22 22 FF FF FF FF 59",
                  "TPM_ID_3":"60 02 22 23 FF FF FF FF 58",
                  "TPM_ID_4":"60 02 22 24 FF FF FF FF 57",
                  "TPM_ID_5":"60 02 22 25 FF FF FF FF 56",
                  "TPM_ID_6":"60 02 22 26 FF FF FF FF 55",
                  "TPM_ID_7":"60 02 22 27 FF FF FF FF 54",  
                  }
     

radio_module = pyLIN.LIN('COM4',19200)

def scheduleActiveMsg():         
    rfr.sendHeader(SLAVE_ADDRESS) 
    return  rfr.readResponse(9)    

def scheduleDiagMsg(msg):
    print msg 
    rfr.sendHeader(0x3C)
    rfr.sendMessage(msg)
    time.sleep(0.25)
    rfr.sendHeader(0x7D)
    return rfr.readResponse(9)  
first_time=True
time_stamp= time.time()    
print "Entering while loop..."
while True:    
    # 10ms loop
    if(time.time() - time_stamp >= ACTIVE_MODE_SLEEP) or first_time==True:                      
        print scheduleActiveMsg()
        time_stamp = time.time()
        first_time= False

radio_module.close()
print "Done !! "


