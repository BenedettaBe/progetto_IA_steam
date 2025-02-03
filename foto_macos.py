import cv2
import time

# Usa il backend AVFoundation per macOS
cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Controlla se la fotocamera si apre correttamente
if not cam.isOpened():
    print("Errore: impossibile aprire la fotocamera.")
    exit()

cv2.namedWindow("Live Camera")

img_counter = 0

# Attendi qualche secondo per l'attivazione della fotocamera
time.sleep(2)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Errore: impossibile acquisire il frame.")
        break

    cv2.imshow("Live Camera", frame)

    k = cv2.waitKey(1)

    if k % 256 == 27:  # Tasto ESC per uscire
        print("Chiusura del programma...")
        break
    elif k % 256 == 32:  # Tasto SPACE per scattare foto
        img_name = f"opencv_frame_{img_counter}.png"
        cv2.imwrite(img_name, frame)
        print(f"Foto salvata: {img_name}")
        img_counter += 1

# Rilascia la fotocamera e chiudi la finestra
cam.release()
cv2.destroyAllWindows()
