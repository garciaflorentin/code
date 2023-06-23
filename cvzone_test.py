from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time
from math import atan2, pi
import math
#import inspire_hand_r

#_inspire_hand_r = inspire_hand_r.InspireHandR()


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5, maxHands=2)


# Serial COM
port = 'COM3'
ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8,
                    stopbits=1, writeTimeout=0, timeout=0)

if ser.is_open:
    print(f"Connexion établie avec succès sur {port}")      
else:
    print(f"Impossible d'établir la connexion sur {port}")

time.sleep(2)
ser.readline()


count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0
count12 = 0
count13 = 0
count14 = 0
count15 = 0


def angle(A, B, C):
    Ax, Ay = A[0]-B[0], A[1]-B[1]
    Cx, Cy = C[0]-B[0], C[1]-B[1]
    a = atan2(Ay, Ax)
    c = atan2(Cy, Cx)
    if a < 0:
        a += pi*2
    if c < 0:
        c += pi*2
    result = (pi*2 + c - a) if a > c else (c - a)
    result *= (180/math.pi)
    if result > 180:
        result = 360 - result
    return result

def map_angle(angle):
    angle_min = 30
    angle_max = 180
    value_min = -1
    value_max = 2000

    # Check if the angle is within the valid range
    if angle < angle_min:
        angle = angle_min
    elif angle > angle_max:
        angle = angle_max

    # Calculate the mapped value
    mapped_value = ((angle - angle_min) / (angle_max - angle_min)) * (value_max - value_min) + value_min

    # Convert the mapped value to a byte sequence
    #byte_value = mapped_value.to_bytes(2, 'big')

    return mapped_value



while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    try:
        if  len(hands) >= 1:

            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # Handtype Left or Right
            if handType1 == 'Left':
                cv2.circle(img, lmList1[8][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[12][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[16][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[20][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[4][:2], 15, (0, 0, 255), -1)
            else: 
                cv2.circle(img, lmList1[8][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList1[12][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList1[16][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList1[20][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList1[4][:2], 15, (0, 255, 255), -1)


            result = dict({'index': angle(lmList1[8][:2], lmList1[6][:2], lmList1[5][:2]),
                           'middle_finger': angle(lmList1[12][:2], lmList1[10][:2], lmList1[9][:2]),
                           'ring_finger': angle(lmList1[16][:2], lmList1[14][:2], lmList1[13][:2]),
                           'little_finger': angle(lmList1[20][:2], lmList1[18][:2], lmList1[17][:2]),
                           'thumb': angle(lmList1[4][:2], lmList1[2][:2], lmList1[1][:2])})



            for key, value in result.items():
                if key == 'index':
                    if value < 180 and 165 < value:
                        # time.sleep(1)
                        if count1 == 15:
                            indexV=map_angle(value)#  ser.write(b'\x01')
                            print(f'key: {key} , value: {value}', 2)
                            count1 == 0
                        else:
                            count1 += 1

                    if value <= 160 and 110 < value:
                        # time.sleep(1)
                        if count2 == 15:
                            indexV=map_angle(value)#  ser.write(b'\x02')
                            count2 == 0
                            print(f'key: {key} , value: {value}', 1)
                        else:
                            count2 += 1

                    if value <= 105 and 0 < value:
                        # time.sleep(1)
                        if count3 == 15:
                            indexV=map_angle(value)#  ser.write(b'\x04')
                            count3 == 0
                            print(f'key: {key} , value: {value}', 0)
                        else:
                            count3 += 1

                if key == 'middle_finger':
                    if value < 180 and 170 < value:
                        if count4 == 10:
                            middle_fingerV=map_angle(value) #   ser.write(b'\x21')
                            count4 == 0
                            print(f'key: {key} , value: {value}', 2)
                        else:
                            count4 += 1

                    if value <= 170 and 115 < value:
                        if count5 == 10:
                            middle_fingerV=map_angle(value)# ser.write(b'\x22')
                            count5 == 0
                            print(f'key: {key} , value: {value}', 1)
                        else:
                            count5 += 1

                    if value <= 105 and 0 < value:
                        if count6 == 10:
                            middle_fingerV=map_angle(value)#ser.write(b'\x24')
                            count6 == 0
                            print(f'key: {key} , value: {value}', 0)
                        else:
                            count6 += 1

                if key == 'ring_finger':
                    if value < 180 and 155 < value:
                        if count7 == 10:
                            ring_fingerV=map_angle(value) # ser.write(b'\x41')
                            count7 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count7 += 1

                    if value <= 145 and 115 < value:
                        if count8 == 10:
                            ring_fingerV=map_angle(value)#  ser.write(b'\x42')
                            count8 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count8 += 1

                    if value <= 105 and 0 < value:
                        if count9 == 10:
                            ring_fingerV=map_angle(value)#   ser.write(b'\x44')
                            count9 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count9 += 1

                if key == 'little_finger':
                    if value < 180 and 155 < value:
                        if count10 == 10:
                            little_fingerV=map_angle(value)#  ser.write(b'\x61')
                            count10 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count10 += 1

                    if value <= 145 and 115 < value:
                        if count11 == 10:
                            little_fingerV=map_angle(value)# ser.write(b'\x62')
                            count11 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count11 += 1

                    if value <= 105 and 0 < value:
                        if count12 == 10:
                            little_fingerV=map_angle(value)#  ser.write(b'\x64')
                            count12 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count12 += 1

                if key == 'thumb':
                    if value < 180 and 165 < value:
                        if count13 == 10:
                            thumbV=map_angle(value)# ser.write(b'\x81')
                            count13 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count13 += 1

                    if value <= 160 and 105 < value:
                        if count14 == 10:
                            thumbV=map_angle(value)# ser.write(b'\x82')
                            count14 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count14 += 1

                    if value <= 100 and 0 < value:
                        if count15 == 10:
                            thumbV=map_angle(value)# ser.write(b'\x84')
                            count15 == 0
                            print(f'key: {key} , value: {value}')
                        else:
                            count15 += 1

        
        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            if handType2 == 'Left':
                cv2.circle(img, lmList2[8][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList2[12][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList2[16][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList2[20][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList2[4][:2], 15, (0, 0, 255), -1)
            else: 
                cv2.circle(img, lmList2[8][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList2[12][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList2[16][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList2[20][:2], 15, (0, 255, 255), -1)
                cv2.circle(img, lmList2[4][:2], 15, (0, 255, 255), -1)

       
      #  _inspire_hand_r.setpos(little_fingerV,middle_fingerV,ring_fingerV,indexV,thumbV)
        

    except:
        continue

        # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
cap.release()
cv2.destroyAllWindows()
