from cgitb import reset
from turtle import delay
from inspire_hand_r import InspireHandR
import time

if __name__=='__main__':
    hand = InspireHandR()
    hand.reset_0()
    hand.set_clear_error()
    #hand.gesture_force_clb()
    #time.sleep(10)

    temp_value = [0,0,0,0,0,0]
    is_static = [0,0,0,0,0,0]
    static_value = [0,0,0,0,0,0]
    a = 1
  

    while a==1:
        value = 0
        temp_value = [0,0,0,0,0,0]
        is_static = [0,0,0,0,0,0]
        static_value = [0,0,0,0,0,0]

        for i in range(200):
            pos_value = i*10
            actforce = hand.get_actforce()
            for i,f in enumerate(actforce[0:4]):
                if is_static[i]:
                    continue
                if f >1000:
                    continue
                if i == 4: #thumbs
                    if f > 400: #If the finger force is greater than 100, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
                     

                elif i!=4:
                    if f > 400: #If the finger force is greater than 50, keep the previous position
                        is_static[i] = 1 #Mark as a static finger, the finger will not move at this position
                        static_value[i] = temp_value[i] #The i-th finger position of the previous step
              

            #pos_value[5] = pos_value[5] + 1000
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
            
            print('pos:',pos1,pos2,pos3,pos4,pos5,pos6)
            print("actforce:", actforce)
            
            #curr_pos = hand.get_actpos()
            #print('currpos',curr_pos)
            time.sleep(0.005)
	
        a = 2
