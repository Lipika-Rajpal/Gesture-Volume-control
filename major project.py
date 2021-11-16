import cv2
import mediapipe as mp
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np                
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
cap = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands= mpHands.Hands()

while True:
     success, img  = cap.read()
     imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
     results = hands.process(imgRGB)

     #print(results.multi_hand_landmarks)
     cv2.rectangle(img, (50,150) , (85,400) , (255,0,12) ,3 )

     if results.multi_hand_landmarks:
         for handLms in results.multi_hand_landmarks:

             lmList = []
             for id, lm in enumerate (handLms.landmark):
                 #print(id ,lm )
                 h , w , c = img.shape
                 cx , cy = int(lm.x*w) , int(lm.y*h)
                 #print(id , cx , cy)
                 lmList.append([id , cx , cy])
                 #print(lmList)


         if lmList : 
                x1, y1 = lmList[4][1] , lmList[4][2]
                x2, y2 = lmList[8][1] , lmList[8][2]
                cv2.circle(img, (x1, y1) , 15 ,(255,0,13), cv2.FILLED)
                cv2.circle(img, (x2, y2) , 15 ,(255,0,13), cv2.FILLED)
                length = math.hypot(x2-x1 , y2-y1)
                #print(length)
                if length < 50 : 
                    z1 = (x1+x2)//2
                    z2 = (y1+y2)//2
                    cv2.circle(img, (z1,z2), 20, (0,0,25), cv2.FILLED)

         vol = np.interp(length, [50,300] , [minVol, maxVol])

         volBar = np.interp( length , [50,200] , [400,150])
         volume.SetMasterVolumeLevel(vol, None)
         
         cv2.rectangle(img, (50,int(volBar) ) , (85,400) , (0,250,12) ,cv2.FILLED )
         
         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS )

     
     
     cv2.imshow("Image" ,img)
     cv2.waitKey(15)

#Vol = 0 ===> MasterVolume = -65
#Vol = 100 ===> MasterVolume = 0
#length 50 to 300 ===> volRange = -65 to 0
#volBar 0 to 100 


