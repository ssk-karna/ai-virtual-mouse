import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

wCam, hCam = 648, 488
frameR = 80

cTime = 0
pTime = 0

smoothening = 6
plocX,plocY = 0,0
clocX,clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

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
        

        #3. Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
    
        #4. Only Index finger : Moving mode
        if fingers[1]==1 and fingers[2]==0:
            #5. Convert coordinates
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            
            #6. Smoothen values

            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening

            #7. Move mouse
            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY = clocX,clocY

        #8. Both index and middle fingers are up
        if fingers[1]==1 and fingers[2]==1:

        #9. Find Distance between fingers
            length,img,lineInfo = detector.findDistance(8,12,img)
        #10. Click mouse if distance short
            if length < 22:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.toggle(down = True)
                    #5. Convert coordinates
                x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
                y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
                
                #6. Smoothen values

                clocX = plocX + (x3-plocX)/smoothening
                clocY = plocY + (y3-plocY)/smoothening

                #7. Move mouse
                autopy.mouse.move(wScr-clocX,clocY)
                
            
            autopy.mouse.toggle(down = False)
   
        #11. Frame Rate
        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    img=cv2.flip(img,1)
    
    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
    (255,0,255),3)
    #12. Display
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)