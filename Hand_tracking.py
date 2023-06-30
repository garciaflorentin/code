import cv2
import serial
import time
from math import atan2, pi
import numpy as np
import math
import inspire_hand_r
import pyrealsense2 as rs
from cvzone.HandTrackingModule import HandDetector

_inspire_hand_r = inspire_hand_r.InspireHandR()
_inspire_hand_r.__init__()

# Initialize the RealSense pipeline and configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.Depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.Color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Serial COM
port = '/dev/ttyUSB0'
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8,
                    stopbits=1, writeTimeout=0, timeout=0)

if ser.is_open:
    print(f"Connexion établie avec succès sur {port}")
else:
    print(f"Impossible d'établir la connexion sur {port}")

time.sleep(2)
ser.readline()


finger_names = ['index', 'middle_finger', 'ring_finger', 'little_finger', 'thumb1','thumb2']
finger_angles = [0, 0, 0, 0, 0,]
finger_counts = [0, 0, 0, 0, 0,0]
finger_threshold = 15
finguer_precision = 50



tempo = 0
count1 = 0
count4 = 0
count7 = 0
count10 = 0
count13 = 0
indexV = 0
middle_fingerV = 0
ring_fingerV = 0
little_fingerV = 0
thumbV = 0

def angle2(A,B,C):

    #les coordonnées x, y et z des points A, B et C
    x_A, y_A, z_A = A[:3]  # Coordonnées du point A
    x_B, y_B, z_B = B[:3]  # Coordonnées du point B
    x_C, y_C, z_C = C[:3]  # Coordonnées du point C

    #Calcul des vecteurs AB et BC
    vec_AB = np.array([x_B - x_A, y_B - y_A, z_B - z_A])
    vec_BC = np.array([x_C - x_B, y_C - y_B, z_C - z_B])

    #Calcul du produit scalaire des vecteurs AB et BC
    dot_product = np.dot(vec_AB, vec_BC)

    #Calcul des normes des vecteurs AB et BC
    norm_AB = np.linalg.norm(vec_AB)
    norm_BC = np.linalg.norm(vec_BC)

    #calcul de l'angle  
    angle_ABC = math.acos(dot_product / (norm_AB * norm_BC))

    #conversion en degree
    result = math.degrees(angle_ABC)

    if result > 180:
        result = 360 - result
    return result






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
    # byte_value = mapped_value.to_bytes(2, 'big')

    int_mapped_value = int(mapped_value)

    return int_mapped_value


while True:
    # Get image frame
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if color_frame is None:
        print("color_frame is empty")
        continue
    color_image = np.asanyarray(color_frame.get_data())
    #Récupération des métadonnées de l'image couleur
    color_profile = color_frame.get_profile()
    #Récupération des informations de calibration
    color_intrinsics = color_profile.as_video_stream_profile().get_intrinsics()
    #Recuperation des informations de transformation entre les images couleur et profondeur
    color_to_depth_extrinsics = depth_profile.get_extrinsics_to(color_profile)
    #Creation d'un facteur d'échelle utilisé pour convertir les valeurs de profondeur brutes (exprimées en unités arbitraires) en valeurs de profondeur en mètres.
    depth_scale = pipeline.get_device().first_depth_sensor().get_depth_scale()


    # Obtenir le cadre de profondeur
    depth_frame = frames.get_depth_frame()
    if depth_frame is None:
        print("depth_frame is empty")
        continue
    #Récupération des métadonnées de l'image de profondeur
    depth_profile = depth_frame.get_profile()
    #Récupération des informations de calibration, pour acceder au paramètres de calibration, y compris les coefficients de distortion.
    depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsics()


    # Find the hand and its landmarks
    hands, img = detector.findHands(color_image)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    try:
        if len(hands) >= 1:

            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # Handtype Left or Right
            # Obtenir la profondeur des points de la main gauche (hand1)
            hand1_point = []

            if handType1 == 'Left':
                cv2.circle(img, lmList1[8][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[12][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[16][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[20][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[4][:2], 15, (0, 0, 255), -1)
            else:   
                continue

            if depth_frame is not None:
                for landmark in lmList1:
                    # Récupérer les coordonnées x et y du landmark
                    landmark_x, landmark_y = landmark[:2]
                    depth_pixel = rs.rs2_project_color_pixel_to_depth_pixel(depth_frame.get_data(), depth_intrinsics, color_intrinsics, color_to_depth_extrinsics, landmark_x, landmark_y, depth_scale)

                    # Obtenir la profondeur à partir du cadre de profondeur
                    landmark_depth = depth_frame.get_distance(landmark_x, landmark_y)
                    hand1_point.append(landmark_x,landmark_y,landmark_depth)

            result = dict({'little_finger': angle(hand1_point[20][:3], hand1_point[18][:3], hand1_point[17][:3]),
                           'middle_finger': angle(hand1_point[16][:3], hand1_point[14][:3], hand1_point[13][:3]),
                           'ring_finger': angle(hand1_point[12][:3], hand1_point[10][:3], hand1_point[9][:3]),
                           'index': angle(hand1_point[8][:3], hand1_point[6][:3], hand1_point[5][:3]),
                           'thumb1': angle(hand1_point[4][:3], hand1_point[3][:3], hand1_point[2][:3]),
                           'tumb2': angle(hand1_point[3][:3], hand1_point[1][:3], hand1_point[0][:3])})

            for i in range(len(finger_names)):

                finger_name = finger_names[i]
                finger_angle = finger_angles[i]
                finger_count = finger_counts[i]

            if finger_name in result:
                
                if finger_count == finger_threshold:
                    
                    temp = finger_angle
                    finger_angle = map_angle(result[finger_name])

                    if not (finger_angle > temp + finguer_precision or finger_angle < temp - finguer_precision):
                        finger_angle = temp

                    print(f'key: {finger_name}, AngleValue: {result[finger_name]}')

                    finger_count = 0

                else:

                    finger_count += 1

            finger_angles[i] = finger_angle
            finger_counts[i] = finger_count

        if tempo == 3:

            _inspire_hand_r.setpos(*finger_angles)
            tempo = 0

        else:

            tempo = tempo + 1

    except:
        continue

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
pipeline.stop()
cv2.destroyAllWindows()
