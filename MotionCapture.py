import cv2
from cvzone.PoseModule import PoseDetector
import socket

cap = cv2.VideoCapture(0)
success, img = cap.read()
h, w, _ = img.shape
detector = PoseDetector()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
    data = []

    if bboxInfo:
        lmString = ''
        for lm in lmList:
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
            data.extend([lm[0], h-lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
