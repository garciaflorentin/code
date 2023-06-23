import serial as s
import time

class InspireHandR:
    def __init__(self):
        #Serial port settings
        port = 'COM3'
        self.ser = s.Serial(port='COM3', baudrate=115200, bytesize=8,stopbits=1, writeTimeout=0, timeout=0)
        self.hand_id = 1
        power1 = 500
        power2 = 500
        power3 = 500
        power4 = 500
        power5 = 500
        power6 = 500
        self.setpower(power1,power2,power3,power4,power5,power6)
        
        speed1 = 1000
        speed2 = 1000
        speed3 = 1000
        speed4 = 1000
        speed5 = 1000 
        speed6 = 1000
        self.setspeed(speed1,speed2,speed3,speed4,speed5,speed6) 

        self.f1_init_pos = 0    #Little finger initial position
        self.f2_init_pos = 0    #Ring finger initial position
        self.f3_init_pos = 0    #Middle finger initial position
        self.f4_init_pos = 0    #Index finger initial position
        self.f5_init_pos = 0   #Thumb finger initial position
        self.f6_init_pos = 0    #Thumb towards palm initial position

        # Hands open, for testing
        # self.f1_init_pos = 0    #Little finger initial position
        # self.f2_init_pos = 0    #Ring finger initial position
        # self.f3_init_pos = 0    #Middle finger initial position
        # self.f4_init_pos = 0    #Index finger initial position
        # self.f5_init_pos = 0    #Thumb finger initial position
        # self.f6_init_pos = 0    #Thumb towards palm initial position

        

    # Divide data into high and low byte
    def data2bytes(self,data):
        rdata = [0xff]*2
        if data == -1:
            rdata[0] = 0xff
            rdata[1] = 0xff
        else:
            rdata[0] = data&0xff
            rdata[1] = (data>>8)&(0xff)
        return rdata

    #Convert hexadecimal or decimal numbers to bytes
    def num2str(self,num):
        str = hex(num)
        str = str[2:4]
        if(len(str) == 1):
            str = '0'+ str
        str = bytearray.fromhex(str) #str.decode(str)      
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

    def setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        global hand_id
        if pos1 <-1 or pos1 >2000:
            print('Data is out of correct range- 1-2000')
            return
        if pos2 <-1 or pos2 >2000:
            print('Data is out of correct range- 1-2000')
            return
        if pos3 <-1 or pos3 >2000:
            print('Data is out of correct range- 1-2000')
            return
        if pos4 <-1 or pos4 >2000:
            print('Data is out of correct range- 1-2000')
            return
        if pos5 <-1 or pos5 >2000:
            print('Data is out of correct range- 1-2000')
            return
        if pos6 <-1 or pos6 >2000:
            print('Data is out of correct range- 1-2000')
            return
        
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
        #print('data sent',putdata)
        
        # print('data sent')
        # for i in range(1,datanum+6):
        #     print(hex(putdata[i-1]))
            
        getdata= self.ser.read(9)
        #print('data returned ',getdata)
        # print('data returned ')
        # for i in range(1,10):
            # print(hex(getdata[i-1]))
        return

    #set angle
    # angle1 = 0  #Little finger straight 1000, bent 0
    # angle2 = 0  #Ring finger straight 1000, bend 0
    # angle3 = 0  #Middle finger straight 1000, bent 0
    # angle4 = 0  #Index finger straight 1000, bent 0
    # angle5 = 1000 #Thumb straight 1000, flexed 0
    # angle6 = 1000 #Thumb turns to palm 0
    # setangle(angle1,angle2,angle3,angle4,angle5,angle6) 

    def setangle(self,angle1,angle2,angle3,angle4,angle5,angle6):
        if angle1 <-1 or angle1 >1000:
            print('Data is out of correct range- 1-1000')
            return
        if angle2 <-1 or angle2 >1000:
            print('Data is out of correct range- 1-1000')
            return
        if angle3 <-1 or angle3 >1000:
            print('Data is out of correct range- 1-1000')
            return
        if angle4 <-1 or angle4 >1000:
            print('Data is out of correct range- 1-1000')
            return
        if angle5 <-1 or angle5 >1000:
            print('Data is out of correct range- 1-1000')
            return
        if angle6 <-1 or angle6 >1000:
            print('Data is out of correct range- 1-1000')
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
        #print('data sent ')
        #for i in range(1,datanum+6):
        #    print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        #print('data returned ')
        #for i in range(1,10):
        #    print(hex(getdata[i-1]))


    #Set the force control threshold
    def setpower(self,power1,power2,power3,power4,power5,power6):
        if power1 <0 or power1 >1000:
            print('Data is out of correct range- 0-1000')
            return
        if power2 <0 or power2 >1000:
            print('Data is out of correct range- 0-1000')
            return
        if power3 <0 or power3 >1000:
            print('Data is out of correct range- 0-1000')
            return
        if power4 <0 or power4 >1000:
            print('Data is out of correct range- 0-1000')
            return
        if power5 <0 or power5 >1000:
            print('Data is out of correct range- 0-1000')
            return
        if power6 <0 or power6 >1000:
            print('Data is out of correct range- 0-1000')
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
        b[7] = self.data2bytes(power1)[0]
        b[8] = self.data2bytes(power1)[1]
        
        b[9] = self.data2bytes(power2)[0]
        b[10] = self.data2bytes(power2)[1]
        
        b[11] = self.data2bytes(power3)[0]
        b[12] = self.data2bytes(power3)[1]
        
        b[13] = self.data2bytes(power4)[0]
        b[14] = self.data2bytes(power4)[1]
        
        b[15] = self.data2bytes(power5)[0]
        b[16] = self.data2bytes(power5)[1]
        
        b[17] = self.data2bytes(power6)[0]
        b[18] = self.data2bytes(power6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        #print('Data sent')
        #for i in range(1,datanum+6):
        #    print(hex(putdata[i-1]))
        
        getdata= self.ser.read(9)
        #print('Returned data ')
        #for i in range(1,10):
        #    print(hex(getdata[i-1]))


    #set speed
    def setspeed(self,speed1,speed2,speed3,speed4,speed5,speed6):
        if speed1 <0 or speed1 >1000:
            print('The data is out of the correct range- 0-1000')
            return
        if speed2 <0 or speed2 >1000:
            print('The data is out of the correct range- 0-1000')
            return
        if speed3 <0 or speed3 >1000:
            print('The data is out of the correct range- 0-1000')
            return
        if speed4 <0 or speed4 >1000:
            print('The data is out of the correct range- 0-1000')
            return
        if speed5 <0 or speed5 >1000:
            print('The data is out of the correct range- 0-1000')
            return
        if speed6 <0 or speed6 >1000:
            print('The data is out of the correct range- 0-1000')
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
            
        getdata = self.ser.read(9)
        '''print('Returned data:')
        for i in range(1,10):
            print(hex(getdata[i-1]))'''

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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
            
        getdata = self.ser.read(20)
        '''print('Returned data:')
        for i in range(1,21):
            print(hex(getdata[i-1]))'''
        
        setpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpos[i-1] = -1
            else:
                setpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpos

    #read setting angle
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(20)
        '''print('Returned data:')
        for i in range(1,21):
            print(hex(getdata[i-1]))'''
        
        
        setangle = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setangle[i-1] = -1
            else:
                setangle[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setangle
    

    #Read the force control threshold set by the driver
    def get_setpower(self):
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(20)
        '''print('Returned data:')
        for i in range(1,21):
            print(hex(getdata[i-1]))'''
        
        setpower = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                setpower[i-1] = -1
            else:
                setpower[i-1] = getdata[i*2+5] + (getdata[i*2+6]<<8)
        return setpower

    #Read the actual position value of the drive
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(20)
        '''print('Returned data:')
        for i in range(1,21):
            print(hex(getdata[i-1]))'''
        
        actpos = [0]*6
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actpos[i-1] = -1
            else:
                actpos[0] = getdata[8] + getdata[7]
                actpos[1] = getdata[10] + getdata[9]
                actpos[2] = getdata[12] + getdata[12]
                actpos[3] = getdata[14] + getdata[13]
                actpos[4] = getdata[16] + getdata[15]
                actpos[5] = getdata[18] + getdata[17]
                #print(type(actforce[0]),eval(actforce[0])
                actpos[0] = actpos[0].encode("hex")
                actpos[1] = actpos[1].encode("hex")
                actpos[2] = actpos[2].encode("hex")
                actpos[3] = actpos[3].encode("hex")
                actpos[4] = actpos[4].encode("hex")
                actpos[5] = actpos[5].encode("hex")

                actpos[0] = int(str(actpos[0]),16)
                actpos[1] = int(str(actpos[1]),16)
                actpos[2] = int(str(actpos[2]),16)
                actpos[3] = int(str(actpos[3]),16)
                actpos[4] = int(str(actpos[4]),16)
                actpos[5] = int(str(actpos[5]),16)

                '''actpos[i-1] = getdata[i*2+5] + (getdata[i*2+6]*(2**8))#<<8)'''
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
                angle[i-1] = getdata[i*2+5] + (getdata[i*2+6]*(2**8))#<<8)
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
        
        getdata = self.ser.read(20)
        # print('Returned data:')
        # for i in range(1,21):
        # print(hex(getdata[i-1]))
        
        actforce = [0]*6

        '''actforce[0] = getdata[8] + getdata[7]
        actforce[1] = getdata[10] + getdata[9]
        actforce[2] = getdata[12] + getdata[12]
        actforce[3] = getdata[14] + getdata[13]
        actforce[4] = getdata[16] + getdata[15]
        actforce[5] = getdata[18] + getdata[17]
        #print(type(actforce[0]),eval(actforce[0])
        actforce[0] = actforce[0].encode("hex")
        actforce[1] = actforce[1].encode("hex")
        actforce[2] = actforce[2].encode("hex")
        actforce[3] = actforce[3].encode("hex")
        actforce[4] = actforce[4].encode("hex")
        actforce[5] = actforce[5].encode("hex")'''
        #actforce = int(actforce,16)
        #actforce = map(int, actforce)
        #print(type(actforce),actforce)
        #actforce[1] = int(actforce[1], 16)
        #print(type(actforce),actforce)
        #print(int(actforce[0]))
       
        for i in range(1,7):
            if getdata[i*2+5]== 0xff and getdata[i*2+6]== 0xff:
                actforce[i-1] = -1
            else:
                actforce[0] = getdata[8] + getdata[7]
                actforce[1] = getdata[10] + getdata[9]
                actforce[2] = getdata[12] + getdata[12]
                actforce[3] = getdata[14] + getdata[13]
                actforce[4] = getdata[16] + getdata[15]
                actforce[5] = getdata[18] + getdata[17]
                #print(type(actforce[0]),eval(actforce[0])
                actforce[0] = actforce[0].encode("hex")
                actforce[1] = actforce[1].encode("hex")
                actforce[2] = actforce[2].encode("hex")
                actforce[3] = actforce[3].encode("hex")
                actforce[4] = actforce[4].encode("hex")
                actforce[5] = actforce[5].encode("hex")

            ''' #getdata[i*2+5] = getdata[i*2+5]
                #getdata[i*2+6] = getdata[i*2+5]
                
                #getdata[i*2+5] = getdata[i*2+5].encode("hex")
                #getdata[i*2+6] = getdata[i*2+6].encode("hex")
                actforce[i-1] = getdata[i*2+5] + (getdata[i*2+6]*(2**8))#<<8)
                #actforce[i-1] = actforce[i-1].encode("hex")
                #print(type(actforce[0]),actforce[0])
                '''
        # The serial port receives an unsigned hexadecimal number consisting of another two bytes. The range of decimal representation is 0 to 65536, while the actual data is signed data, indicating different directions of force, and the range is -32768~ 32767,
        # Therefore, it is necessary to process the received data to obtain the data of the actual force sensor: when the reading is greater than 32767, subtract 65536 from the number of times.
        for i in range(len(actforce)):
            actforce[i] = int(actforce[i], 16)
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(20)
        '''print('Returned data:')
        for i in range(1,21):
            print(hex(getdata[i-1]))'''
        
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(14)
        '''print('Returned data:')
        for i in range(1,15):
            print(hex(getdata[i-1]))'''
        
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(14)
        '''print('Returned data:')
        for i in range(1,15):
            print(hex(getdata[i-1]))'''
        
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(14)
        '''print('Returned data:')
        for i in range(1,15):
            print(hex(getdata[i-1]))'''
        
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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(9)
        '''print('Returned data:')
        for i in range(1,10):
            print(hex(getdata[i-1]))'''


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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(18)
        '''print('Returned data:')
        for i in range(1,19):
            print(hex(getdata[i-1]))'''

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
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
        
        getdata = self.ser.read(18)
        '''print('Returned data:')
        for i in range(1,19):
            print(hex(getdata[i-1]))'''
            
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
        
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
            
        getdata = self.ser.read(9)
        '''print('Returned data:')
        for i in range(1,10):
            print(hex(getdata[i-1]))'''
    
    #Set the upper power control threshold
    def setdefaultpower(self,power1,power2,power3,power4,power5,power6):
        if power1 <0 or power1 >1000:
            print('Data out of the correct range: 0-1000')
            return
        if power2 <0 or power2 >1000:
            return
        if power3 <0 or power3 >1000:
            return
        if power4 <0 or power4 >1000:
            return
        if power5 <0 or power5 >1000:
            return
        if power6 <0 or power6 >1000:
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
        b[7] = self.data2bytes(power1)[0]
        b[8] = self.data2bytes(power1)[1]
        
        b[9] = self.data2bytes(power2)[0]
        b[10] = self.data2bytes(power2)[1]
        
        b[11] = self.data2bytes(power3)[0]
        b[12] = self.data2bytes(power3)[1]
        
        b[13] = self.data2bytes(power4)[0]
        b[14] = self.data2bytes(power4)[1]
        
        b[15] = self.data2bytes(power5)[0]
        b[16] = self.data2bytes(power5)[1]
        
        b[17] = self.data2bytes(power6)[0]
        b[18] = self.data2bytes(power6)[1]
        
        #checksum
        b[19] = self.checknum(b,datanum+4)
        
        #Send data to serial port
        putdata = b''
        
        for i in range(1,datanum+6):
            putdata = putdata + self.num2str(b[i-1])
        self.ser.write(putdata)
        '''print('Data sent:')
        for i in range(1,datanum+6):
            print(hex(putdata[i-1]))'''
            
        getdata = self.ser.read(9)
        '''print('Returned data:')
        for i in range(1,10):
            print(hex(getdata[i-1]))'''

    def soft_setpos(self,pos1,pos2,pos3,pos4,pos5,pos6):
        value0 = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]
        pos_value = [pos1,pos2,pos3,pos4,pos5,pos6]
        n = 5
      
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
                if i ==5:#thumbs
                    if f >300: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
                else:
                    if f >300: #If the finger force is greater than 50, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
            temp_value = pos_value
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
            #toc = time.time()
            #print('ii: %d,toc=%f'%(ii,toc - tic))


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
