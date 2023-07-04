import cv2
import serial
import time
from math import atan2, pi
import numpy as np
import math
import inspire_hand_rTest
import pyrealsense2 as rs
from cvzone.HandTrackingModule import HandDetector

_inspire_hand_r = inspire_hand_rTest.InspireHandR()
_inspire_hand_r.__init__()

# Initialize the RealSense pipeline and configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

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
finger_angles = [0, 0, 0, 0, 0]
finger_counts = [0, 0, 0, 0, 0, 0]
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

def angle2(A, B, C):
    # les coordonnées x, y et z des points A, B et C
    x_A, y_A, z_A = A[:3]  # Coordonnées du point A
    x_B, y_B, z_B = B[:3]  # Coordonnées du point B
    x_C, y_C, z_C = C[:3]  # Coordonnées du point C

    # Calcul des vecteurs AB et BC
    vec_AB = np.array([x_B - x_A, y_B - y_A, z_B - z_A])
    vec_BC = np.array([x_C - x_B, y_C - y_B, z_C - z_B])

    # Calcul du produit scalaire des vecteurs AB et BC
    dot_product = np.dot(vec_AB, vec_BC)

    # Calcul des normes des vecteurs AB et BC
    norm_AB = np.linalg.norm(vec_AB)
    norm_BC = np.linalg.norm(vec_BC)

    # calcul de l'angle
    angle_ABC = math.acos(dot_product / (norm_AB * norm_BC))

    # conversion en degrés
    result = math.degrees(angle_ABC)

    if result > 180:
        result = 360 - result
    return result


def angle(A, B, C):
    Ax, Ay = A[0] - B[0], A[1] - B[1]
    Cx, Cy = C[0] - B[0], C[1] - B[1]
    return math.atan2(Cy, Cx) - math.atan2(Ay, Ax)

try:
    while True:
        # Attendre une nouvelle frame du pipeline
        frames = pipeline.wait_for_frames()

        # Récupérer la frame de profondeur et de couleur
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Vérifier que les deux frames sont valides
        if not depth_frame or not color_frame:
            continue

        # Convertir les frames en images numpy
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Détecter les mains dans l'image couleur
        hands, color_image = detector.findHands(color_image)

        if len(hands) > 0:
            hand_landmarks = hands[0]['lmList']  # Coordonnées des landmarks de la main détectée
            hand_box = hands[0]['bbox']  # Boîte englobante de la main détectée

            # Récupérer les coordonnées x et y du landmark de l'index
            index_x, index_y = hand_landmarks[8][1], hand_landmarks[8][2]

            # Récupérer les informations de calibration de profondeur
            depth_profile = depth_frame.profile
            depth_intrinsics = depth_profile.as_video_stream_profile().intrinsics

            # Récupérer les informations de calibration de couleur
            color_profile = color_frame.profile
            color_intrinsics = color_profile.as_video_stream_profile().intrinsics

            # Récupérer les extrinsèques de couleur à profondeur
            color_to_depth_extrinsics = color_profile.get_extrinsics_to(depth_profile)

            # Récupérer l'échelle de profondeur
            depth_scale = pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
            # Récupérer la valeur de profondeur correspondante au pixel projeté
            depth_value = depth_frame.get_distance(depth_pixel[0], depth_pixel[1])

            # Projeter les coordonnées du pixel de couleur sur l'image de profondeur
            depth_point = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [index_x, index_y], depth_value)         
            depth_pixel = rs.rs2_project_point_to_pixel(color_intrinsics, depth_profile)
            
            # Afficher les coordonnées et la valeur de profondeur
            print(f"Coordonnées (x, y) de l'index : ({index_x}, {index_y})")
            print(f"Coordonnées projetées (x, y) sur l'image de profondeur : ({depth_pixel[0]}, {depth_pixel[1]})")
            print(f"Valeur de profondeur : {depth_value}")

        # Afficher l'image couleur avec les repères des mains
        cv2.imshow("Color Image", color_image)

        # Quitter la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Arrêter le pipeline RealSense et fermer les fenêtres OpenCV
    pipeline.stop()
    cv2.destroyAllWindows()
    ser.close()
