import inspire_hand_rTest
import time
import cv2
import serial
from math import atan2, pi
import numpy as np
import math
import pyrealsense2 as rs
from cvzone.HandTrackingModule import HandDetector


class Type_of_grasping():

   _inspire_hand_r = inspire_hand_rTest.InspireHandR()

   def tog(self,objet_tyoe):

    # Chemin vers les fichiers de configuration et de poids du modèle
    config_path ='/Desktop/stage_bristol/code_/models/ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8/pipeline.config'
    weight_path = '/Desktop/stage_bristol/code_/models/ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8/model.ckpt'


    # Chargement du modèle
    net = cv2.dnn.readNetFromCaffe(config_path, weight_path)

    # Liste des classes d'objets que le modèle peut détecter
    classes = [
        'classe 0',
        'classe 1',
        'classe 2',
        # Ajoutez les classes supplémentaires ici
    ]

    # Chargement de la vidéo d'entrée
    video_path = 'chemin/vers/video.mp4'
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        # Lecture de la frame de la vidéo
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionnement de la frame pour le traitement plus rapide
        resized_frame = cv2.resize(frame, (300, 300))

        # Conversion de l'image en un blob
        blob = cv2.dnn.blobFromImage(resized_frame, 0.007843, (300, 300), 127.5)

        # Passage du blob à travers le réseau de neurones pour obtenir les détections
        net.setInput(blob)
        detections = net.forward()

        # Parcours des détections et affichage des résultats
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filtrer les détections avec une confiance minimale
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                class_label = classes[class_id]
                x1 = int(detections[0, 0, i, 3] * frame.shape[1])
                y1 = int(detections[0, 0, i, 4] * frame.shape[0])
                x2 = int(detections[0, 0, i, 5] * frame.shape[1])
                y2 = int(detections[0, 0, i, 6] * frame.shape[0])

                # Dessiner le cadre et le label de la détection sur l'image
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Affichage de la frame résultante
        cv2.imshow('Object Detection', frame)

        # Sortir de la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()

        