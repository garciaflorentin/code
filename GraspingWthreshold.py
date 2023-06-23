import inspire_hand_r
import time
_inspire_hand_r = inspire_hand_r.InspireHandR()

_inspire_hand_r.__init__()
#_inspire_hand_r.gesture_force_clb()
#_inspire_hand_r.set_clear_error()
#_inspire_hand_r.reset()

#time.sleep(10)
pos_litF=2000
pos_midF=2000
pos_ringF=2000
pos_index=2000
pos_thumb1=0
pos_thumb2=0
_inspire_hand_r.setpos(0,0,0,0,0,0)
time.sleep(2)


for i in range(0,20):
   pos_thumb2=(i+1)*100
   print("force thumb2:",_inspire_hand_r.get_actforce()[5])

   if _inspire_hand_r.get_actforce()[5] < 15:
      print("force thumb2:",_inspire_hand_r.get_actforce()[5])
      _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)

for i in range(0,20):
   pos_thumb1=(i+1)*100
   print("force thumb1:",_inspire_hand_r.get_actforce()[4])

   if _inspire_hand_r.get_actforce()[4] < 15:
      print("force thumb1:",_inspire_hand_r.get_actforce()[4])
      _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)
      _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)



# for i in range(1,101):
#    _inspire_hand_r.setpos(2000,1000,2000,1000,0,0)

