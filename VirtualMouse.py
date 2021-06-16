import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

wCam,hCam = 648,488
frameR = 100

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
cTime = 0
pTime = 0

wScr, hScr = autopy.screen.size()

detector = htm.handDetector(maxHands=1)
while True:
    #1. Get hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)

    lmlist,bbox = detector.findPosition(img)

    if len(lmlist) != 0:
        #2. Check the tip of the index and middle fingers
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        #print(x1,y1,x2,y2)

        #3. Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        #print(fingers)
        #4. Only Index finger : Moving mode
        if fingers[1]==1 and fingers[2]==0:
            #5. Convert coordinates
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))

            
            #6. Smoothen values
            #7. Move mouse
            autopy.mouse.move(wScr-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
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