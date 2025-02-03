# Questo script utilizza la libreria OpenCV per catturare e visualizzare il flusso video dalla webcam.
# Permette di scattare foto premendo il tasto "Space" e di visualizzare il video in tempo reale.
# Ogni foto scattata viene salvata con un nome che include un contatore incrementale (ad esempio: opencv_frame_0.png).
# Il ciclo si interrompe premendo il tasto "Escape"
import cv2

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
