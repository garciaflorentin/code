import pyrealsense2 as rs
import cv2
import numpy as np

def main():
    # Initialisation de la caméra RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)


    # Démarrer le flux vidéo
    pipeline.start(config)

    try:
        while True:
            # Attendre une nouvelle image
            frames = pipeline.wait_for_frames()

            # Obtenir l'image couleur à partir du flux
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if not color_frame:
                continue

            if not depth_frame:
                print("depth_frame is empty")
                continue

            # Convertir l'image couleur en tableau NumPy
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            # Afficher l'image en temps réel
            cv2.imshow('Camera RealSense', color_image)
            cv2.imshow('Depth Data', depth_image)
            # Appuyez sur 'q' pour quitter la boucle
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Arrêter le flux vidéo et fermer la fenêtre
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
