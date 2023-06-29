import inspire_hand_rTest
import time



class GraspingWthreshold():

   _inspire_hand_r = inspire_hand_rTest.InspireHandR()

   def Grasp(self):

      self._inspire_hand_r.setforce(150,150,150,150,150,150)
      """ _inspire_hand_r.reset()
      time.sleep(3)

      _inspire_hand_r.set_clear_error()
      time.sleep(3)

      _inspire_hand_r.__init__()
      time.sleep(5) 
      """
      """ _inspire_hand_r.gesture_force_clb()
      time.sleep(5)  """


      #_inspire_hand_r.set_clear_error()
      #time.sleep(3)
      #_inspire_hand_r.gesture_force_clb()
      #time.sleep(5)
      threshold = 100


      pos_litF=0
      pos_midF=0
      pos_ringF=0
      pos_index=0
      pos_thumb1=0
      pos_thumb2=0
      self._inspire_hand_r.setpos(0,0,0,0,0,0)
      #time.sleep(1)
      '''for i in range(2000):
         print(_inspire_hand_r.get_actforce())'''

      tempo_litF=0
      tempo_midF=0
      tempo_ringF=0
      tempo_index=0
      tempo_thumb1=0
      tempo_thumb2=0




      for i in range(0,50):

         print("force :",self._inspire_hand_r.get_actforce())
         print("t2")

         if self._inspire_hand_r.get_actforce()[5] <threshold:
            tempo_thumb2=0
            pos_thumb2=pos_thumb2+50
            self._inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)
         else:
            if tempo_thumb2<3:
               pos_thumb2=pos_thumb2+50
               self._inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)
               tempo_thumb2=tempo_thumb2+1


      """ for i in range(0,50):

         print("force :",_inspire_hand_r.get_actforce())
         print("t1")

         if _inspire_hand_r.get_actforce()[4] <threshold:
            tempo_thumb1=0
            pos_thumb1=pos_thumb1+50
            _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)
         else:
            if tempo_thumb1<3:
               pos_thumb1=pos_thumb1+50
               _inspire_hand_r.setpos(0,0,0,0,pos_thumb1,pos_thumb2)
               tempo_thumb1=tempo_thumb1+1 """


      for i in range(0,50):

         print("force :",self._inspire_hand_r.get_actforce())
         incr=50
         

         if self._inspire_hand_r.get_actforce()[4] <threshold:
            tempo_thumb1=0
            pos_thumb1=pos_thumb1+50
         else:
            if tempo_thumb1<3:
               pos_thumb1=pos_thumb1+50
               tempo_thumb1=tempo_thumb1+1

         if self._inspire_hand_r.get_actforce()[3] <threshold:
            tempo_index=0
            pos_index=pos_index+50
         else:
            if tempo_index<3:
               pos_index=pos_index+50
               tempo_index=tempo_index+1

         if self._inspire_hand_r.get_actforce()[2] <threshold:
            tempo_ringF=0
            pos_ringF=pos_ringF+50
         else:
            if tempo_ringF<3:
               pos_ringF=pos_ringF+50
               tempo_ringF=tempo_ringF+1

         if self._inspire_hand_r.get_actforce()[1] <threshold:
            tempo_midF=0
            pos_midF=pos_midF+50
         else:
            if tempo_midF<3:
               pos_midF=pos_midF+50
               tempo_midF=tempo_midF+1  

         if self._inspire_hand_r.get_actforce()[0] <threshold:
            tempo_litF=0
            pos_litF=pos_litF+50
         else:
            if tempo_litF<3:
               pos_litF=pos_litF+50
               tempo_litF=tempo_litF+1 



         self._inspire_hand_r.setpos(pos_litF,pos_midF,pos_ringF,pos_index,pos_thumb1,pos_thumb2)

      # _inspire_hand_r.soft_setpos(0,0,0,0,0,0)
      # time.sleep(3)
      # _inspire_hand_r.soft_setpos(0,0,0,0,0,2000)
      # time.sleep(1)
      # _inspire_hand_r.soft_setpos(1000,1000,1000,1000,1000,2000)


   def GraspPos(self,pos_litF_,pos_midF_,pos_ringF_,pos_index_,pos_thumb1_,pos_thumb2_):

      pos_litF=0
      pos_midF=0
      pos_ringF=0
      pos_index=0
      pos_thumb1=0
      pos_thumb2=0

      self._inspire_hand_r = inspire_hand_rTest.InspireHandR()
      self._inspire_hand_r.setpos(0,0,0,0,0,0)
      time.sleep(2) 

      self._inspire_hand_r.setforce(150,150,150,150,150,150)
      threshold = 100
      tempo_litF=0
      tempo_midF=0
      tempo_ringF=0
      tempo_index=0
      tempo_thumb1=0
      tempo_thumb2=0

      range_=2

      for i in range(0,range_):

         print("force :",self._inspire_hand_r.get_actforce())
         values = [pos_litF_,pos_midF_,pos_ringF_,pos_index_,pos_thumb1_,pos_thumb2_]
         max_value = max(values)
         incr= max_value/range_
         vitesse = self.scale_value(max_value)
         self._inspire_hand_r.setspeed(vitesse,vitesse,vitesse,vitesse,vitesse,vitesse)
         
         if self._inspire_hand_r.get_actforce()[5] <threshold:
            tempo_thumb2=0
            if pos_thumb2<pos_thumb2_:
             pos_thumb2=pos_thumb2+incr
             if pos_thumb2/pos_thumb2_>0:
                pos_thumb2=pos_thumb2_
         else:
            if tempo_thumb2<1:
               if pos_thumb2<pos_thumb2_:
                pos_thumb2=pos_thumb2+incr
                if pos_thumb2/pos_thumb2_>0:
                  pos_thumb2=pos_thumb2_
               tempo_thumb2=tempo_thumb2+1


         if self._inspire_hand_r.get_actforce()[4] <threshold:
            tempo_thumb1=0
            if pos_thumb1<pos_thumb1_:
             pos_thumb1=pos_thumb1+incr
             if pos_thumb1/pos_thumb1_>0:
                pos_thumb1=pos_thumb1_
         else:
            if tempo_thumb1<1:
               if pos_thumb1<pos_thumb1_:
                  pos_thumb1=pos_thumb1+incr
                  if pos_thumb1/pos_thumb1_>0:
                     pos_thumb1=pos_thumb1_
               tempo_thumb1=tempo_thumb1+1

         if self._inspire_hand_r.get_actforce()[3] <threshold:
            tempo_index=0
            if pos_index<pos_index_:
                pos_index=pos_index+incr
                if pos_index/pos_index_>0:
                  pos_index=pos_index_
         else:
            if tempo_index<1:
               if pos_index<pos_index_:
                pos_index=pos_index+incr
                if pos_index/pos_index_>0:
                  pos_index=pos_index_
               tempo_index=tempo_index+1

         if self._inspire_hand_r.get_actforce()[2] <threshold:
            tempo_ringF=0
            if pos_ringF<pos_ringF_:
                pos_ringF=pos_ringF+incr
                if pos_ringF/pos_ringF_>0:
                  pos_ringF=pos_ringF_
         else:
            if tempo_ringF<1:
               if pos_ringF<pos_ringF_:
                pos_ringF=pos_ringF+incr
                if pos_ringF/pos_ringF_>0:
                  pos_ringF=pos_ringF_
               tempo_ringF=tempo_ringF+1

         if self._inspire_hand_r.get_actforce()[1] <threshold:
            tempo_midF=0
            if pos_midF<pos_midF_:
                pos_midF=pos_midF+incr
                if pos_midF/pos_midF_>0:
                  pos_midF=pos_midF_
         else:
            if tempo_midF<1:
               if pos_midF<pos_midF_:
                pos_midF=pos_midF+incr
                if pos_midF/pos_midF_>0:
                  pos_midF=pos_midF_
               tempo_midF=tempo_midF+1  

         if self._inspire_hand_r.get_actforce()[0] <threshold:
            tempo_litF=0
            if pos_litF<pos_litF_:
                pos_litF=pos_litF+incr
                if pos_litF/pos_litF_>0:
                  pos_litF=pos_litF_
         else:
            if tempo_litF<1:
               if pos_litF<pos_litF_:
                pos_litF=pos_litF+incr
                if pos_litF/pos_litF_>0:
                  pos_litF=pos_litF_
               tempo_litF=tempo_litF+1 



         self._inspire_hand_r.setpos(pos_litF,pos_midF,pos_ringF,pos_index,pos_thumb1,pos_thumb2)

   def scale_value(self,value):
      min_value = 0
      max_value = 2000
      new_min = 0
      new_max = 1000

      scaled_value = (value - min_value) * (new_max - new_min) / (max_value - min_value) + new_min
      return scaled_value
