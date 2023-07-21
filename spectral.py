import xiapi
import numpy as np
import cv2
import spectral as spy

# Kameraverbindung öffnen
cam = xiapi.Camera()
cam.open_device()

# Bildgröße und Farbkanalmodus einstellen
cam.set_imgdataformat('XI_MONO16')
cam.set_width(640)
cam.set_height(480)

# Anzahl der spektralen Bänder und Mosaik-Anordnung (5x5 Pixel Mosaik)
num_spectral_bands = 25
mosaic_order = [(i % 5) * 5 + (i // 5) for i in range(num_spectral_bands)]

# Videostream starten
cam.start_acquisition()

# Array für die gesamten Hyperspektraldaten erstellen
spectral_data = np.empty((cam.get_height(), cam.get_width(), num_spectral_bands), dtype=np.uint16)

# Schleife zum Erfassen der Hyperspektraldaten
for i in range(num_spectral_bands):
    # Einzelbild vom Videostream erfassen
    img = xiapi.Image()
    cam.get_image(img)
    data = img.get_image_data_numpy()

    # Hyperspektrale Daten speichern und neu anordnen
    spectral_data[:, :, mosaic_order[i]] = data

# Videostream beenden und Kameraverbindung schließen
cam.stop_acquisition()
cam.close_device()

# Daten mit Spectral Python verarbeiten
# Hier können Sie spektrale Analysen, Visualisierungen usw. mit den neu angeordneten hyperspektralen Daten durchführen

# Beispiel: Erstellen Sie ein RGB-Bild durch Kombination der ersten 3 Bänder
rgb_image = spectral_data[:, :, :3]

# Beispiel: Anzeigen des RGB-Bildes mit OpenCV
cv2.imshow('Hyperspektraldaten', rgb_image)

# Auf 'q' drücken, um das Fenster zu schließen
cv2.waitKey(0)
cv2.destroyAllWindows()
