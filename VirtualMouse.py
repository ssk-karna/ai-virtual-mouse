import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

wCam,hCam = 648,488

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
cTime = 0
pTime = 0

detector = htm.handDetector()
while True:
    #1. Get hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)


    #2. Check the tip of the index and middle fingers
    fingers = detector.fingersUp()
    print(fingers)
    #3. Check which fingers are up
    #4. Only Index finger : Moving mode
    #5. Convert coordinates
    #6. Smoothen values
    #7. Move mouse
    #8. Both index and middle fingers are up
    #9. Find Distance between fingers
    #10. Click mouse if distance short

    #11. Frame Rate
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
    (255,0,255),3)
    #12. Display


    cv2.imshow("Image",img)
    cv2.waitKey(1)