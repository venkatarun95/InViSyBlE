import numpy as np
import cv2

import cProfile
import re

from Scheduler import Scheduler
from GetFrame import GetFrame
from FaceDetector import FaceDetector

#from GetBWFrame import GetBWFrame
#from SIFTKeypoints import SIFTKeypoints
import SIFTObjectDetector
import FaceRecognizer


def runInViSyBlE():
    SIFTObjectDetector.loadDatabase("/home/venkat/Documents/Projects/InViSyBle/ObjectDatabase/")
    FaceRecognizer.loadDatabase("/home/venkat/Documents/Projects/InViSyBle/FaceDatabase/")

    #cap = cv2.VideoCapture(0)
    #getFrame = GetFrame()
    #getBWFrame = GetBWFrame()
    scheduler = Scheduler()
    scheduler.updateComputationList([GetFrame, SIFTObjectDetector.SIFTObjectDetector, FaceDetector, FaceRecognizer.FaceRecognizer])

    while(True):#cap.isOpened()):
        #ret, frame = cap.read()

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = getFrame((0,0), None)
        #frame, frameId = getBWFrame(frame, None)
        res = scheduler.compute()
        if None in res:
            continue
        frame, frameId = res[0]
        detectedObjects = res[1]
        detectedFaces = res[3]

        #draw face rectangles
        faces = res[2]
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow('frame',frame)
        print detectedObjects, detectedFaces
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #cap.release()
    cv2.destroyAllWindows()

#cProfile.run('re.compile(runInViSyBlE())')
runInViSyBlE()