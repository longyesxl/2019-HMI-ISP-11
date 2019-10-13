import requests
import sys
from json import JSONDecoder
import cv2
import os
from sys import platform
import time

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e
cap=cv2.VideoCapture(0)
params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True
params["hand_detector"] = 2
params["body"] = 0
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
handRectangles = [
        # Left/Right hands person 0
        [
        op.Rectangle(0., 0., 0., 0.),
        op.Rectangle(160., 80., 320., 320.),
        ]
]
pointpair=[[20,19],
[19,18],
[18,17],
[17,0],
[16,15],
[15,14],
[14,13],
[13,0],
[12,11],
[11,10],
[10,9],
[9,0],
[8,7],
[7,6],
[6,5],
[5,0],
[4,3],
[3,2],
[2,1],
[1,0],
[17,13],
[13,9],
[9,5],
[5,1]]
while True:
    st=time.time()
    ret ,frame = cap.read()
    datum = op.Datum()
    datum.cvInputData = frame
    datum.handRectangles = handRectangles
    opWrapper.emplaceAndPop([datum])
    #cv2.rectangle(frame,(80,40),(240,200),(0,0,255),3)
    cv2.rectangle(frame,(160,80),(480,400),(0,0,255),3)
    ok=True
    for point in datum.handKeypoints[1][0]:
        if(point[2]>0.05):
            cv2.circle(frame,(int(point[0]),int(point[1])),4,(255,0,0),2)
        else:
            ok=False
    if(ok):
        for pair in pointpair:
            pt1=datum.handKeypoints[1][0][pair[0]]
            pt2=datum.handKeypoints[1][0][pair[1]]
            ptt1=(int(pt1[0]),int(pt1[1]))
            ptt2=(int(pt2[0]),int(pt2[1]))
            cv2.line(frame,ptt1,ptt2,(0,255,0),2)    
    cv2.imshow("capture", frame)
    cv2.waitKey(1)
    ed=time.time()
    print(ed-st)
