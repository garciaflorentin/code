import pyrealsense2 as rs

def main():
    # Initialiser le contexte RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Démarrer le flux vidéo
    pipeline.start(config)
    
    # Obtenir les informations du premier périphérique RealSense connecté
    devices = pipeline.query_devices()
    if len(devices) > 0:
        device = devices[0]
        print("Nom du périphérique:", device.get_info(rs.camera_info.name))
        print("Série du périphérique:", device.get_info(rs.camera_info.serial_number))
        print("Firmware version:", device.get_info(rs.camera_info.firmware_version))
    else:
        print("Aucun périphérique RealSense détecté.")
    
    # Arrêter le flux vidéo et fermer le contexte RealSense
    pipeline.stop()
    
if __name__ == "__main__":
    main()
