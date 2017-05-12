"""

This is LIN communication module compatible with FTDI chip.

@author: pdesai

"""
import serial

class LIN():
 
    BREAK_TIMING = 1/1000.0 # 1msec instead of 14/19200
    SYNC_BYTE = 0x55
    def __init__(self,portnum,baud=19200):
        self.__portNumber=portnum
        try:
            self.__portInstance=serial.Serial(self.__portNumber,baud,timeout=0.1)
        except IOError as e:            
            print (e)
        
    def close(self):
        self.__portInstance.close()
 
    def byteToHex( self,byteStr ):
        '''
        Convert a byte string to it's hex string representation e.g. for output.
        
        Uses list comprehension which is a fractionally faster implementation than
        the alternative, more readable, implementation below
        
           hex = []
           for aChar in byteStr:
               hex.append( "%02X " % ord( aChar ) )
        
           return ''.join( hex ).strip()
        '''
        return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

    def hexToByte( self,hexStr ):
        '''
        Convert a string hex byte values into a byte string. The Hex Byte values may
        or may not be space separated.
        
        The list comprehension implementation is fractionally slower in this case
        
           hexStr = ''.join( hexStr.split(" ") )
           return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
                                          for i in range(0, len( hexStr ), 2) ] )
        '''
        dbytes = [] 
        hexStr = ''.join( hexStr.split(" ") )

        for i in range(0, len(hexStr), 2):
            dbytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

        return ''.join( dbytes )
    
    def sendHeader(self,address):        
        self.__portInstance.sendBreak(self.BREAK_TIMING)
        self.__portInstance.write(chr(self.SYNC_BYTE))
        self.__portInstance.write(chr(address)) 
  
  
    def readResponse(self,readlen):
        # Flush all input buffers 
        self.__portInstance.flushInput()
        '''
        Important :
        In case of a LIN transceiver, the transmitter pin is connected 
        back to receiver pin for diagnostic purposes. 
        
        Hence, the first 2 bytes read will result in SYNC (0x55) & 
        Address(transmitted in header) bytes.
        
        For the actual message, we read these 2 bytes and discard them.        
        '''        
        self.__portInstance.read(2)
        return self.byteToHex(self.__portInstance.read(readlen))
          
                      
    def sendMessage(self,msg):
        if(0== self.__portInstance.write(self.hexToByte(msg))):
            print ("Write error : flushing I/O buffers")
            self.__portInstance.flushInput()
            self.__portInstance.flushOutput()


version='0.1'
