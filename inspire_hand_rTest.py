import serial as s
import struct
#import numpy 
#import string
#import binascii
import time
import copy

class InspireHandR:
    def __init__(self):
        #Serial port settings
        self.ser=s.Serial('/dev/ttyUSB0',115200)
        self.ser.isOpen()
        self.hand_id = 1
        force1 = 400
        force2 = 400
        force3 = 400
        force4 = 400
        force5 = 400
        force6 = 800
        self.setforce(force1,force2,force3,force4,force5,force6)
        
        speed1 = 1000
        speed2 = 1000
        speed3 = 1000
        speed4 = 1000
        speed5 = 1000
        speed6 = 1000
        self.setspeed(speed1,speed2,speed3,speed4,speed5,speed6) 

        self.f1_init_pos = 400    #Little finger initial position
        self.f2_init_pos = 400    #Ring finger initial position
        self.f3_init_pos = 400    #Middle finger initial position
        self.f4_init_pos = 400    #Index finger initial position
        self.f5_init_pos = 1200   #Thumb finger initial position
        self.f6_init_pos = 700    #Thumb towards palm initial position

        self.reset()

    # Divide data into high and low byte
    def data2bytes(self,data):
        rdata = [0xff]*2
        if data == -1:
            rdata[0] = 0xff
            rdata[1] = 0xff
        else:
            rdata[0] = int(data) & 0xff
            rdata[1] = (int(data) >> 8) & 0xff

        return rdata

    #Convert hexadecimal or decimal numbers to bytes
    def num2str(self,num):
        str = hex(num)
        str = str[2:4]
        if(len(str) == 1):
            str = '0'+ str
        str = bytes.fromhex(str)     
        #print(str)
        return str

    #checksum
    def checknum(self,data,leng):
        result = 0
        for i in range(2,leng):

            result += data[i]
        result = result&0xff
        #print(result)
        return result

    # Setting Position
    def setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        global hand_id
        if pos1 <-1 or pos1 >2000:
            if pos1<-1:
                pos1=-1
            else:
                pos1=2000
            #print('Data is out of correct range：-1-2000')
                        #return

        if pos2 <-1 or pos2 >2000:
            if pos2<-1:
                pos2=-1
            else:
                pos2=2000
            #print('Data is out of correct range：-1-2000')
                        #return

        if pos3 <-1 or pos3 >2000:
            if pos3<-1:
                pos3=-1
            else:
                pos3=2000
           # print('Data is out of correct range：-1-2000')
                       #return

        if pos4 <-1 or pos4 >2000:
            if pos4<-1:
                pos4=-1
            else:
                pos4=2000
            #print('Data is out of correct range：-1-2000')
                        #return

        if pos5 <-1 or pos5 >2000:
            if pos5<-1:
                pos5=-1
            else:
                pos5=2000
           # print('Data is out of correct range：-1-2000')
            #return

        if pos6 <-1 or pos6 >2000:
            if pos6<-1:
                pos6=-1
            else:
                pos6=2000
            #print('Data is out of correct range：-1-2000')
            #return
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id 
        b[2] = self.hand_id

        #number of data
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xC2
        b[6] = 0x05
        
        #data
        b[7] = self.data2bytes(pos1)[0]
        b[8] = self.data2bytes(pos1)[1]
        
        b[9] = self.data2bytes(pos2)[0]
        b[10] = self.data2bytes(pos2)[1]
        
        b[11] = self.data2bytes(pos3)[0]
        b[12] = self.data2bytes(pos3)[1]
        
        b[13] = self.data2bytes(pos4)[0]
        b[14] = self.data2bytes(pos4)[1]
        
        b[15] = self.data2bytes(pos5)[0]
        b[16] = self.data2bytes(pos5)[1]
        
        b[17] = self.data2bytes(pos6)[0]
        b[18] = self.data2bytes(pos6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        #print('data sent：',putdata)
        
        # print('data sent：')
        # for i in range(1,datanum+6):
        #     print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        #print('data returned：',getdata)
        # print('data returned：')
        # for i in range(1,10):
            # print(hex(getdata[i-1]))
        return

    #set angle
    def setangle(self,angle1,angle2,angle3,angle4,angle5,angle6):
        if angle1 <-1 or angle1 >1000:
            print('Data is out of correct range：-1-1000')
            return
        if angle2 <-1 or angle2 >1000:
            print('Data is out of correct range：-1-1000')
            return
        if angle3 <-1 or angle3 >1000:
            print('Data is out of correct range：-1-1000')
            return
        if angle4 <-1 or angle4 >1000:
            print('Data is out of correct range：-1-1000')
            return
        if angle5 <-1 or angle5 >1000:
            print('Data is out of correct range：-1-1000')
            return
        if angle6 <-1 or angle6 >1000:
            print('Data is out of correct range：-1-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xCE
        b[6] = 0x05
        
        #data
        b[7] = self.data2bytes(angle1)[0]
        b[8] = self.data2bytes(angle1)[1]
        
        b[9] = self.data2bytes(angle2)[0]
        b[10] = self.data2bytes(angle2)[1]
        
        b[11] = self.data2bytes(angle3)[0]
        b[12] = self.data2bytes(angle3)[1]
        
        b[13] = self.data2bytes(angle4)[0]
        b[14] = self.data2bytes(angle4)[1]
        
        b[15] = self.data2bytes(angle5)[0]
        b[16] = self.data2bytes(angle5)[1]
        
        b[17] = self.data2bytes(angle6)[0]
        b[18] = self.data2bytes(angle6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('data sent：')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        print('data returned：')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))


    #Set the force control threshold
    def setforce(self,force1,force2,force3,force4,force5,force6):
        if force1 <0 or force1 >1000:
            print('Data is out of correct range：0-1000')
            return
        if force2 <0 or force2 >1000:
            print('Data is out of correct range：0-1000')
            return
        if force3 <0 or force3 >1000:
            print('Data is out of correct range：0-1000')
            return
        if force4 <0 or force4 >1000:
            print('Data is out of correct range：0-1000')
            return
        if force5 <0 or force5 >1000:
            print('Data is out of correct range：0-1000')
            return
        if force6 <0 or force6 >1000:
            print('Data is out of correct range：0-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xDA
        b[6] = 0x05
        
        #data
        b[7] = self.data2bytes(force1)[0]
        b[8] = self.data2bytes(force1)[1]
        
        b[9] = self.data2bytes(force2)[0]
        b[10] = self.data2bytes(force2)[1]
        
        b[11] = self.data2bytes(force3)[0]
        b[12] = self.data2bytes(force3)[1]
        
        b[13] = self.data2bytes(force4)[0]
        b[14] = self.data2bytes(force4)[1]
        
        b[15] = self.data2bytes(force5)[0]
        b[16] = self.data2bytes(force5)[1]
        
        b[17] = self.data2bytes(force6)[0]
        b[18] = self.data2bytes(force6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        print('Returned data:')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))


    #set speed
    def setspeed(self,speed1,speed2,speed3,speed4,speed5,speed6):
        if speed1 <0 or speed1 >1000:
            print('The data is out of the correct range：0-1000')
            return
        if speed2 <0 or speed2 >1000:
            print('The data is out of the correct range：0-1000')
            return
        if speed3 <0 or speed3 >1000:
            print('The data is out of the correct range：0-1000')
            return
        if speed4 <0 or speed4 >1000:
            print('The data is out of the correct range：0-1000')
            return
        if speed5 <0 or speed5 >1000:
            print('The data is out of the correct range：0-1000')
            return
        if speed6 <0 or speed6 >1000:
            print('The data is out of the correct range：0-1000')
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xF2
        b[6] = 0x05
        
        #data
        b[7] = self.data2bytes(speed1)[0]
        b[8] = self.data2bytes(speed1)[1]
        
        b[9] = self.data2bytes(speed2)[0]
        b[10] = self.data2bytes(speed2)[1]
        
        b[11] = self.data2bytes(speed3)[0]
        b[12] = self.data2bytes(speed3)[1]
        
        b[13] = self.data2bytes(speed4)[0]
        b[14] = self.data2bytes(speed4)[1]
        
        b[15] = self.data2bytes(speed5)[0]
        b[16] = self.data2bytes(speed5)[1]
        
        b[17] = self.data2bytes(speed6)[0]
        b[18] = self.data2bytes(speed6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
            
        getdata = self.ser.read(9)
        print('Returned data:')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))

    #Read the actual position value of the drive
    def get_setpos(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0xC2
        b[6] = 0x05
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        #print('Data sent: ',putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
            
        getdata = self.ser.read(20)
        print('Returned data:')
        #for i in range(1,21):
            #print(hex(getdata[i-1]))
        
        setpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpos[i-1] = -1
            else:
                setpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpos

    #read set angle values
    def get_setangle(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0xCE
        b[6] = 0x05
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(20)
        print('Returned data:')
        #for i in range(1,21):
            #print(hex(getdata[i-1]))
        
        
        setangle = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setangle[i-1] = -1
            else:
                setangle[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setangle
    

    #Read the force control threshold set
    def get_setforce(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0xDA
        b[6] = 0x05
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(20)
        print('Returned data:')
        #for i in range(1,21):
            #print(hex(getdata[i-1]))
        
        setpower = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpower[i-1] = -1
            else:
                setpower[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpower

    #Read the actual position value
    def get_actpos(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0xFE
        b[6] = 0x05
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(20)
        print('Returned data:')
        #for i in range(1,21):
            #print(hex(getdata[i-1]))
        
        actpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actpos[i-1] = -1
            else:
                actpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return actpos

   #Read the actual angle value
    def get_actangle(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x0A
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        # print('Data sent:')
        # for i in range(1,datanum+6):
        # print(hex(putdata[i-1]))
        
        getdata = self.ser.read(20)
        # print('Returned data:')
        # for i in range(1,21):
        # print(hex(getdata[i-1]))
        
        angle = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                angle[i-1] = -1
            else:
                angle[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return angle

    #Read the actual force
    def get_actforce(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x2E
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        # print('Data sent:')
        # for i in range(1,datanum+6):
        # print(hex(putdata[i-1]))
        #time.sleep(0.1)

        getdata = self.ser.read(20)
        # print('Returned data:')
        # for i in range(1,21):
        # print(hex(getdata[i-1]))
        
        actforce = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actforce[i-1] = -1
            else:
                actforce[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        
        # The serial port receives an unsigned hexadecimal number consisting of another two bytes. The range of decimal representation is 0 to 65536, while the actual data is signed data, indicating different directions of force, and the range is -32768~ 32767,
        # Therefore, it is necessary to process the received data to obtain the data of the actual force sensor: when the reading is greater than 32767, subtract 65536 from the number of times.
        for i in range(len(actforce)):
            if actforce[i] > 32767:
                actforce[i] = actforce[i] - 65536
        return actforce

    #read current
    def get_current(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x3A
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x0C
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(20)
        print('Returned data:')
        #for i in range(1,21):
            #print(hex(getdata[i-1]))
        
        current = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                current[i-1] = -1
            else:
                current[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return current

    #read failure information
    def get_error(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x46
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x06
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(14)
        print('Returned data:')
        #for i in range(1,15):
            #print(hex(getdata[i-1]))
        
        error = [0]*6
        for i in range(1,7):
            error[i-1] = getdata[i+6]
        return error

    #read status information
    def get_status(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x4C
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x06
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
            self.ser.write(putdata)
        print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))
        
        getdata = self.ser.read(14)
        print('Returned data:')
        for i in range(1,15):
            print(hex(getdata[i-1]))
        
        status = [0]*6
        for i in range(1,7):
            status[i-1] = getdata[i+6]
        return status
        

    #read temperature information
    def get_temp(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #read operation
        b[4] = 0x11
        
        #start address
        b[5] = 0x52
        b[6] = 0x06
        
        #read the length of the register
        b[7] = 0x06
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(14)
        print('Returned data:')
        #for i in range(1,15):
            #print(hex(getdata[i-1]))
        
        temp = [0]*6
        for i in range(1,7):
            temp[i-1] = getdata[i+6]
        return temp


    # clear errors
    def set_clear_error(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #Start address
        b[5] = 0xEC
        b[6] = 0x03
        
        #data
        b[7] = 0x01
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(9)
        print('Returned data:')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))


   #Save parameters to FLASH
    def set_save_flash(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xED
        b[6] = 0x03
        
        #data
        b[7] = 0x01
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(18)
        print('Returned data:')
        #for i in range(1,19):
            #print(hex(getdata[i-1]))

    #Reset Parameter
    def get_reset_param(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xEE
        b[6] = 0x03
        
        #data
        b[7] = 0x01
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(18)
        print('Returned data:')
        #for i in range(1,19):
            #print(hex(getdata[i-1]))

    #force sensor calibration
    def gesture_force_clb(self):
        datanum = 0x04
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0xF1
        b[6] = 0x03
        
        #data
        b[7] = 0x01
        
        #checksum
        b[8] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
        
        getdata = self.ser.read(18)
        print('Returned data:')
        #for i in range(1,19):
            #print(hex(getdata[i-1]))
            
    #Set the power-on speed
    def setdefaultspeed(self,speed1,speed2,speed3,speed4,speed5,speed6):
        if speed1 <0 or speed1 >1000:
            print('Data out of the correct range: 0-1000')
            return
        if speed2 <0 or speed2 >1000:
            return
        if speed3 <0 or speed3 >1000:
            return
        if speed4 <0 or speed4 >1000:
            return
        if speed5 <0 or speed5 >1000:
            return
        if speed6 <0 or speed6 >1000:
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0x08
        b[6] = 0x04
        
        #data
        b[7] = self.data2bytes(speed1)[0]
        b[8] = self.data2bytes(speed1)[1]
        
        b[9] = self.data2bytes(speed2)[0]
        b[10] = self.data2bytes(speed2)[1]
        
        b[11] = self.data2bytes(speed3)[0]
        b[12] = self.data2bytes(speed3)[1]
        
        b[13] = self.data2bytes(speed4)[0]
        b[14] = self.data2bytes(speed4)[1]
        
        b[15] = self.data2bytes(speed5)[0]
        b[16] = self.data2bytes(speed5)[1]
        
        b[17] = self.data2bytes(speed6)[0]
        b[18] = self.data2bytes(speed6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
            
        getdata = self.ser.read(9)
        print('Returned data:')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))
    
    #Set the upper power control threshold
    def setdefaultforce(self,force1,force2,force3,force4,force5,force6):
        if force1 <0 or force1 >1000:
            print('Data out of the correct range: 0-1000')
            return
        if force2 <0 or force2 >1000:
            return
        if force3 <0 or force3 >1000:
            return
        if force4 <0 or force4 >1000:
            return
        if force5 <0 or force5 >1000:
            return
        if force6 <0 or force6 >1000:
            return
        
        datanum = 0x0F
        b = [0]*(datanum + 5)
        #frame header
        b[0] = 0xEB
        b[1] = 0x90

        #hand_id number
        b[2] = self.hand_id

        #data count
        b[3] = datanum
        
        #write operation
        b[4] = 0x12
        
        #start address
        b[5] = 0x14
        b[6] = 0x04
        
        #data
        b[7] = self.data2bytes(force1)[0]
        b[8] = self.data2bytes(force1)[1]
        
        b[9] = self.data2bytes(force2)[0]
        b[10] = self.data2bytes(force2)[1]
        
        b[11] = self.data2bytes(force3)[0]
        b[12] = self.data2bytes(force3)[1]
        
        b[13] = self.data2bytes(force4)[0]
        b[14] = self.data2bytes(force4)[1]
        
        b[15] = self.data2bytes(force5)[0]
        b[16] = self.data2bytes(force5)[1]
        
        b[17] = self.data2bytes(force6)[0]
        b[18] = self.data2bytes(force6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        print('Data sent:')
        #for i in range(1,datanum+6):
            #print(hex(putdata[i-1]))
            
        getdata = self.ser.read(9)
        #print('Returned data:')
        #for i in range(1,10):
            #print(hex(getdata[i-1]))

    def soft_setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        value0 = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]
        pos_value = [pos1,pos2,pos3,pos4,pos5,pos6]
        #n = 5
        #diffpos = pos1 - self.f1_init_pos
        tic = time.time()
        for ii in range(5):
            # self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            # print('============================')
            actforce = self.get_actforce()
            print('actforce: ',actforce )
            for i,f in enumerate(actforce[0:5]):
                if is_static[i]:
                    continue
                if f >1000:
                    continue
                if i == 4:#thumbs
                    if f > 100: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
                else:
                    if f > 100: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
            
            temp_value = pos_value.copy()
            for i in range(6):
                if is_static[i]:
                    pos_value[i] = static_value[i]

            pos1 = pos_value[0] #The little finger is straightened by 0 and bent by 2000
            pos2 = pos_value[1] #The ring finger is straightened by 0 and bent by 2000
            pos3 = pos_value[2] #The middle finger is straightened by 0 and bent by 2000
            pos4 = pos_value[3] #Forefinger straightens 0, bends 2000
            pos5 = pos_value[4] #The thumb is straightened by 0 and bent by 2000
            pos6 = pos_value[5] #The thumb turns to the palm 2000
            self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            toc = time.time()
            actpos = self.get_actpos()
            print("act_pos: ", actpos)
            print('ii: %d,toc=%f'%(ii,toc - tic))


    def reset(self):
        pos1 = self.f1_init_pos #The little finger is straightened by 0 and bent by 2000
        pos2 = self.f2_init_pos #Ring finger straight 0, bend 2000
        pos3 = self.f3_init_pos #Middle finger straight 0, bend 2000
        pos4 = self.f4_init_pos #Forefinger straight 0, bend 2000
        pos5 = self.f5_init_pos #Thumb straight 0, bend 2000
        pos6 = self.f6_init_pos #thumb to palm 2000
        self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
        return

    def reset_0(self):
        pos1 = 0 #The little finger is straightened by 0 and bent by 2000
        pos2 = 0 #Ring finger straight 0, bend 2000
        pos3 = 0 # middle finger straight 0, bend 2000
        pos4 = 0 #Forefinger straightens 0, bends 2000
        pos5 = 0# thumb straight 0, bend 2000
        pos6 = 0 #thumb to palm 2000
        self.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
        return


'''if __name__ == "__main__":
    hand = InspireHandR()
    power1 = 400
    power2 = 400
    power3 = 400
    power4 = 400
    power5 = 400
    power6 = 800
    hand.setpower(power1,power2,power3,power4,power5,power6)

    speed1 = 1000
    speed2 = 1000
    speed3 = 1000
    speed4 = 1000
    speed5 = 1000
    speed6 = 500
    hand.setspeed(speed1,speed2,speed3,speed4,speed5,speed6)
    temp_value = [0,0,0,0,0,0]
    is_static = [0,0,0,0,0,0]
    static_value = [0,0,0,0,0,0]
    tforce = 100
    a = 1

    while a==1:
        value0 = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]

        for i in range(100):
            value = 10*i
            pos_value = [value]*6 #The theoretical position of the next step of 6 fingers
            actforce = hand.get_actforce()
            for i,f in enumerate(actforce[0:5]):
                if is_static[i]:
                    continue
                if f >1000:
                    continue
                if i == 4: #thumbs
                    if f >100: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
                        
                else:
                    if f >100: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step


            pos_value[5] = pos_value[5] + 700
            if pos_value[4] >2000: pos_value[4] =2000
            if pos_value[5] >2000: pos_value[5] =2000
            temp_value = pos_value.copy()
            
            for i in range(6):
                if is_static[i]:
                    pos_value[i] = static_value[i]

            pos1 = pos_value[0] #The little finger is straightened by 0 and bent by 2000
            pos2 = pos_value[1] #The ring finger is straightened by 0 and bent by 2000
            pos3 = pos_value[2] #The middle finger is straightened by 0 and bent by 2000
            pos4 = pos_value[3] #Forefinger straightens 0, bends 2000
            pos5 = pos_value[4] #The thumb is straightened by 0 and bent by 2000
            pos6 = pos_value[5] #The thumb turns to the palm 2000
            hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            print('44444444444444444444444444')
            print('pos:',pos1,pos2,pos3,pos4,pos5,pos6)
            print("actforce:", actforce)
            print('5555555555555555')
            curr_pos = hand.get_actpos()
            print('currpos',curr_pos)
            time.sleep(0.005)
        
        time.sleep(2)
        hand.reset_0()
        #time.sleep(2)
        hand.set_clear_error()
        
        a = 2'''        