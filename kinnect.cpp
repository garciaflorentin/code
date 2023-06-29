#include <iostream>
#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/registration.h>

#ifdef _WIN32
    #include <conio.h>  // Pour Windows
#else
    #include <unistd.h>
    #include <termios.h>    
#endif

bool isKeyPressed() {
#ifdef _WIN32
    return _kbhit();  // Pour Windows
#else
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    int ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return ch == 32;  // Pour les autres systèmes
#endif
}

int main() {
    // Création de l'instance du gestionnaire Kinect
    libfreenect2::Freenect2 freenect2;
    libfreenect2::Freenect2Device* device = nullptr;

    // Vérification de la présence d'un capteur Kinect v2
    if (freenect2.enumerateDevices() == 0) {
        std::cerr << "Aucun capteur Kinect v2 détecté." << std::endl;
        return 1;
    }

    // Ouverture du capteur Kinect v2
    std::string serial = freenect2.getDefaultDeviceSerialNumber();
    device = freenect2.openDevice(serial);
    if (!device) {
        std::cerr << "Impossible d'ouvrir le capteur Kinect v2." << std::endl;
        return 1;
    }

    // Configuration des canaux de données
    libfreenect2::SyncMultiFrameListener listener(libfreenect2::Frame::Color | libfreenect2::Frame::Depth);
    libfreenect2::FrameMap frames;

    // Démarrage de la capture
    device->setColorFrameListener(&listener);
    device->setIrAndDepthFrameListener(&listener);
    device->start();

    while (true) {
        // Attente de l'arrivée de nouveaux frames
        listener.waitForNewFrame(frames);

        // Récupération des frames couleur et profondeur
        libfreenect2::Frame* colorFrame = frames[libfreenect2::Frame::Color];
        libfreenect2::Frame* depthFrame = frames[libfreenect2::Frame::Depth];

        // Accès aux données des frames
        unsigned char* colorData = colorFrame->data;
        unsigned short* depthData = (unsigned short*)depthFrame->data;

        // Faites quelque chose avec les données ici, par exemple enregistrez-les sur le disque

        // Affichage de la résolution des frames
        int colorWidth = colorFrame->width;
        int colorHeight = colorFrame->height;
        int depthWidth = depthFrame->width;
        int depthHeight = depthFrame->height;
        std::cout << "Résolution des frames couleur : " << colorWidth << "x" << colorHeight << std::endl;
        std::cout << "Résolution des frames profondeur : " << depthWidth << "x" << depthHeight << std::endl;

        // Libération des frames
        listener.release(frames);

        // Condition d'arrêt du programme (par exemple, appuyez sur une touche pour sortir)
        // Remplacez cela par votre propre condition de sortie si nécessaire
        if (isKeyPressed()) {
            break;
        }
    }

    // Arrêt de la capture et fermeture du capteur Kinect v2
    device->stop();
    device->close();

    return 0;
}
