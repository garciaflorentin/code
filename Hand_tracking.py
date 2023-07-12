import cv2
import serial
import time
from math import atan2, pi
import numpy as np
import math
import inspire_hand_rTest
import pyrealsense2 as rs
from cvzone.HandTrackingModule import HandDetector
import GraspingWthreshold
import socket
import subprocess

# Initialize the RealSense pipeline and configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)


tcp1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_ip = socket.gethostname()         #Any interface
port = 5000        #Arbitrary non-privileged port
buffer_size = 1024
tcp1.bind ((tcp_ip , port))
tcp1.listen(1)
#subprocess.Popen(["python3", "app.py"])

con, addr = tcp1.accept()
print ("TCP Connection from: ", addr)


grasp = GraspingWthreshold.GraspingWthreshold()
_inspire_hand_r = inspire_hand_rTest.InspireHandR()
_inspire_hand_r.__init__()



# Initialize the hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)
# Serial COM
port = '/dev/ttyUSB0'
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8,stopbits=1, writeTimeout=0, timeout=0)

if ser.is_open:
    print(f"Connexion établie avec succès sur {port}")
else:
    print(f"Impossible d'établir la connexion sur {port}")

time.sleep(2)
ser.readline()


finger_names = ['index', 'middle_finger', 'ring_finger', 'little_finger', 'thumb1','thumb2']
finger_angles = [0, 0, 0, 0, 0, 0]
finger_counts = [0, 0, 0, 0, 0, 0]
finger_threshold = 0
finguer_precision = 0#35
deadzone_finger= 100
deadzone_thumb1= 150
deadzone_thumb2= 400

wrist_position = np.zeros((1,3))
smoothing_factor= 1 #0.6
previous_angles = np.zeros((6,1))
blocked_finger = [[0] * 6 for _ in range(2)]
temps_attente_us = 80000  # Temps en microsecondes
dernier_temps = 0


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

def quantification_angle(finger_angle):
    if finguer_precision == 0:
        return finger_angle
    rounded_angle = round(finger_angle / finguer_precision) * finguer_precision
    return int(rounded_angle)


def angle2(A, B, C):
    # Les coordonnées x, y et z des points A, B et C
    x_A, y_A, z_A = A[:3]  # Coordonnées du point A
    x_B, y_B, z_B = B[:3]  # Coordonnées du point B
    x_C, y_C, z_C = C[:3]  # Coordonnées du point C

    # Calcul des vecteurs AB et BC
    vec_AB = np.array([x_B - x_A, y_B - y_A, z_B - z_A])
    vec_BC = np.array([x_C - x_B, y_C - y_B, z_C - z_B])

    # Calcul des normes des vecteurs AB et BC
    norm_AB = np.linalg.norm(vec_AB)
    norm_BC = np.linalg.norm(vec_BC)

    # Calcul de l'angle en utilisant atan2
    cross_product = np.cross(vec_AB, vec_BC)
    dot_product = np.dot(vec_AB, vec_BC)

    angle_ABC = math.atan2(np.linalg.norm(cross_product), dot_product)

    # Conversion en degrés
    result = math.degrees(angle_ABC)

    if result > 180:
        result = 360 - result

    return result


def convert_color_pixel_to_depth_pixel(depth_frame, depth_intrinsics, color_intrinsics, color_to_depth_extrinsics, x, y, depth_scale):
    depth_pixel = rs.rs2_project_color_pixel_to_depth_pixel(
        np.array([x, y]), depth_frame.get_data(), depth_scale, 0, 0, depth_intrinsics, color_intrinsics, color_to_depth_extrinsics, None, None)
    return depth_pixel



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


def map_angle(angle,finger_type):

    angle_min = 20
    angle_max = 150
    value_min = 0
    value_max = 2000

    if finger_type == 'thumb1':

        angle_min = 20
        angle_max = 60
        value_min = 0
        value_max = 2000

    if finger_type =='thumb2':

        angle_min = 20
        angle_max = 30
        value_min = 0
        value_max = 2000



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

    con, addr = tcp1.accept()

    # Get image frame
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if color_frame is None:
        print("color_frame is empty")
        continue

    if depth_frame is None:
        print("depth_frame is empty")
        continue

    color_image = np.asanyarray(color_frame.get_data())
    #Récupération des métadonnées de l'image couleur et distance
    color_profile = color_frame.get_profile()
    depth_profile = depth_frame.get_profile()
    #Récupération des informations de calibration
    color_intrinsics = color_profile.as_video_stream_profile().get_intrinsics()
    #Recuperation des informations de transformation entre les images couleur et profondeur
    color_to_depth_extrinsics = depth_profile.get_extrinsics_to(color_profile)
    depth_to_color_extrinsics = color_profile.get_extrinsics_to(depth_profile)
    #Creation d'un facteur d'échelle utilisé pour convertir les valeurs de profondeur brutes (exprimées en unités arbitraires) en valeurs de profondeur en mètres.
    depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

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
            hand1_point = np.zeros((21, 3))
            
            """ if handType1 == 'Left':
                cv2.circle(img, lmList1[8][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[12][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[16][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[20][:2], 15, (0, 0, 255), -1)
                cv2.circle(img, lmList1[4][:2], 15, (0, 0, 255), -1) """
                

            if depth_frame is not None:

                for i, landmark in enumerate(lmList1):

                    landmark_x, landmark_y = landmark[:2]
                    landmark_depth = depth_frame.get_distance(landmark_x, landmark_y)
                    hand1_point[i] = [landmark_x, landmark_y, landmark_depth]

                wrist_position= hand1_point[0][:2]
                """wrist_depth = hand1_point[0][2]  # Récupérer la dernière donnée de profondeur de hand1_point
                inverse_depth = 1/wrist_depth  # Calculer la valeur inversée
                circle_radius = int(inverse_depth * 20)  # Ajuster le rayon du cercle en fonction de inverse_depth """
                cv2.circle(img, tuple(map(int, wrist_position)), 15 , (0, 0, 255), -1)
                cv2.putText(img, f'Wrist Position: {wrist_position}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)
                Wrist_Depth = "{:.{}f}".format(hand1_point[0][2], 2)
                cv2.putText(img, f'Wrist Depth:{Wrist_Depth}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0, 255), 2)




                if (time.perf_counter() * 1e6) - dernier_temps >= temps_attente_us:

                    angles = [
                    angle2(hand1_point[20][:3], hand1_point[18][:3], hand1_point[17][:3]),
                    angle2(hand1_point[16][:3], hand1_point[14][:3], hand1_point[13][:3]),
                    angle2(hand1_point[12][:3], hand1_point[10][:3], hand1_point[9][:3]),
                    angle2(hand1_point[8][:3], hand1_point[6][:3], hand1_point[5][:3]),
                    angle2(hand1_point[4][:3], hand1_point[3][:3], hand1_point[2][:3]),
                    angle2(hand1_point[3][:3], hand1_point[1][:3], hand1_point[0][:3])]
                    result = dict(zip(finger_names, angles))                     
                    #print(result)
                    # Mettre à jour l'angle précédent
                    previous_angles = finger_angles

                    for i, finger_name in enumerate(finger_names):

                        finger_angle = finger_angles[i]
                        finger_count = finger_counts[i]

                        if finger_name in result:
                            if finger_count == finger_threshold:
                                temp = finger_angle
                                finger_angle = map_angle(result[finger_name], finger_name)

                                # Lissage des angles
                                finger_angleSmooth = smoothing_factor * finger_angle + (1 - smoothing_factor) * previous_angles[i]
                                finger_angle = quantification_angle(int(finger_angleSmooth))

                                # Vérifier la précision de l'angle
                                if finger_name == 'thumb1':
                                    if abs(finger_angle - previous_angles[i]) <= deadzone_thumb1:
                                        finger_angle = previous_angles[i]  # Ignorer la mise à jour de l'angle
                                elif finger_name == 'thumb2':
                                    if abs(finger_angle - previous_angles[i]) <= deadzone_thumb2:
                                        finger_angle = previous_angles[i]  # Ignorer la mise à jour de l'angle
                                # Vérifier si la différence est inférieure à la zone morte
                                else:
                                    if abs(finger_angle - previous_angles[i]) <= deadzone_finger:
                                        finger_angle = previous_angles[i]  # Ignorer la mise à jour de l'angle

                                
                                finger_count = 0
                            else:
                                finger_count += 1

                        finger_angles[i] = finger_angle
                        finger_counts[i] = finger_count

                    #_inspire_hand_r.setpos(*finger_angles)

                    data = con.recv(buffer_size).decode('utf-8')  # Recevoir les données (1024 est la taille du tampon)
                    if data == b'NULL':
                        print('NULL')
                    # Traitez les données reçues selon vos besoins
                    # if-else pour exécuter soit l'action correspondante soit grasp.GraspPos3(...)
                    if data == b'open':
                        print('open')
                    elif data == b'close':
                        print('close')
                        # ...
                    elif data == b'ok':
                        print('ok')
                        # ...
                    elif data == b'grasp2':
                        print('grasp2')
                        # ...       
                    elif data == b'grasp5':
                        print('grasp5')
                        # ...       
                    elif data == b'rock':
                        print('rock')
                        # ...                                                                   
                    else:
                        # Exécutez la ligne grasp.GraspPos3(...) par défaut
                        grasp.GraspPos3(_inspire_hand_r, *finger_angles, *previous_angles, blocked_finger)
                    dernier_temps = time.perf_counter() * 1e6  # Récupérer le temps actuel en microsecondes

                    #for ligne in blocked_finger:
                    #   print('#',ligne)
                    
    except:
        continue 
        

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

pipeline.stop()
cv2.destroyAllWindows()
ser.close()
tcp1.close()
con.close()