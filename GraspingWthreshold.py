import inspire_hand_r
import time
_inspire_hand_r = inspire_hand_r.InspireHandR()

_inspire_hand_r.reset()
time.sleep(3)
_inspire_hand_r.set_clear_error()
time.sleep(3)

_inspire_hand_r.__init__()
time.sleep(5)
_inspire_hand_r.gesture_force_clb()
time.sleep(10)



pos_litF=0
pos_midF=0
pos_ringF=0
pos_index=0
pos_thumb1=0
pos_thumb2=0
_inspire_hand_r.setpos(0,0,0,0,0,0)


for i in range(0,10):

   print("force :",_inspire_hand_r.get_actforce())

   if _inspire_hand_r.get_actforce()[5] <15:
      pos_thumb2=(i+1)*100
      _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)



for i in range(0,10):

   print("force :",_inspire_hand_r.get_actforce())

   if _inspire_hand_r.get_actforce()[4] <15:
      pos_thumb1=(i+1)*100
      _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)


for i in range(0,10):

   print("force :",_inspire_hand_r.get_actforce())


   if _inspire_hand_r.get_actforce()[3] <15:
      pos_index=(i+1)*100
   if _inspire_hand_r.get_actforce()[2] <15:
      pos_ringF=(i+1)*100
   if _inspire_hand_r.get_actforce()[1] <15:
      pos_midF=(i+1)*100   
   if _inspire_hand_r.get_actforce()[0] <15:
      pos_litF=(i+1)*100   
   _inspire_hand_r.setpos(pos_litF,pos_midF,pos_ringF,pos_index,pos_thumb1,pos_thumb2)

# _inspire_hand_r.soft_setpos(0,0,0,0,0,0)
# time.sleep(3)
# _inspire_hand_r.soft_setpos(0,0,0,0,0,2000)
# time.sleep(1)
# _inspire_hand_r.soft_setpos(1000,1000,1000,1000,1000,2000)


