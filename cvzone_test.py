from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time
from math import atan2, pi
import math
import inspire_hand_r

_inspire_hand_r = inspire_hand_r.InspireHandR()
_inspire_hand_r.__init__()


cap = cv2.VideoCapture('/dev/video0')
detector = HandDetector(detectionCon=0.5, maxHands=2)


# Serial COM
port ='/dev/ttyUSB0'
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8,
                    stopbits=1, writeTimeout=0, timeout=0)

if ser.is_open:
    print(f"Connexion établie avec succès sur {port}")      
else:
    print(f"Impossible d'établir la connexion sur {port}")

time.sleep(2)
ser.readline()

tempo=0
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
indexV=0
middle_fingerV=0
ring_fingerV=0
little_fingerV=0
thumbV=0




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
    angle_min = 50
    angle_max = 165
    value_min = 2000
    value_max = 0

    # Check if the angle is within the valid range
    if angle < angle_min:
        angle = angle_min
    elif angle > angle_max:
        angle = angle_max


    # Calculate the mapped value
    mapped_value = ((angle - angle_min) / (angle_max - angle_min)) * (value_max - value_min) + value_min

    # Convert the mapped value to a byte sequence
    #byte_value = mapped_value.to_bytes(2, 'big')

    int_mapped_value = int(mapped_value)

    return int_mapped_value



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

            precision=50

            for key, value in result.items():
                if key == 'index':
                        # time.sleep(1)
                        if count1 == 15:
                            temp=indexV
                            indexV= map_angle(value)#  ser.write(b'\x01')
                            if not(indexV > temp + precision or indexV <temp-precision) :
                                 indexV=temp
                                 
                            #print(f'key: {key} , value: {indexV}')
                            print(f'key: {key} , ANGLEvalue: {value}')
                            count1 == 0
                        else:
                            count1 += 1


                if key == 'middle_finger':
                        if count4 == 15:
                            temp=middle_fingerV
                            middle_fingerV= map_angle(value)#  ser.write(b'\x01')
                            if not(middle_fingerV > temp + precision or middle_fingerV <temp-precision) :
                                 middle_fingerV=temp
                            count4 == 0
                            #print(f'key: {key} , value: {middle_fingerV}')
                            print(f'key: {key} , ANGLEvalue: {value}')

                        else:
                            count4 += 1

                if key == 'ring_finger':
                        if count7 == 15:
                            temp=ring_fingerV
                            ring_fingerV= map_angle(value)#  ser.write(b'\x01')
                            if not(ring_fingerV > temp + precision or ring_fingerV <temp-precision) :
                                 ring_fingerV=temp
                            count7 == 0
                            #print(f'key: {key} , value: {ring_fingerV}')
                            print(f'key: {key} , ANGLEvalue: {value}')

                        else:
                            count7 += 1

                if key == 'little_finger':
                        if count10 == 15:
                            temp=little_fingerV
                            little_fingerV= map_angle(value)#  ser.write(b'\x01')
                            if not(little_fingerV > temp + precision or little_fingerV <temp-precision) :
                                 little_fingerV=temp
                            count10 == 0
                            #print(f'key: {key} , value: {little_fingerV}')
                            print(f'key: {key} , ANGLEvalue: {value}')

                        else:
                            count10 += 1

                    
                if key == 'thumb':
                        if count13 == 15:
                            temp=thumbV
                            thumbV= map_angle(value)#  ser.write(b'\x01')
                            if not(thumbV > temp + precision or thumbV <temp-precision) :
                                 thumbV=temp
                            count13 == 0
                            #print(f'key: {key} , value: {thumbV}')
                            print(f'key: {key} , ANGLEvalue: {value}')

                        else:
                            count13 += 1

        
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

        if tempo == 3:
            _inspire_hand_r.setpos(little_fingerV,ring_fingerV,middle_fingerV,indexV,thumbV,0)
            #_inspire_hand_r.setpos(0,1000,0,100.50,0,0)
            tempo=0
        else:
            tempo=tempo+1


    except:
        continue

        # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
cap.release()
cv2.destroyAllWindows()
