#import requests
import sys
from json import JSONDecoder
import cv2
import os
from sys import platform
import time
import serial #导入模块


# Import Openpose (Windows/Ubuntu/OSX)
def limitit(data,maxd,mind):
    if data>maxd:
        return maxd
    elif data<mind:
        return mind
    else :
        return data
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
portx="COM4"
  #波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
bps=9600
  #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
timex=5
  # 打开串口，并得到串口对象
ser=serial.Serial(portx,bps,timeout=timex)
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
        pp=datum.handKeypoints[1][0]
        l1s=pp[20][1]-pp[17][1]
        l1x=pp[17][1]-pp[0][1]
        l1=l1s/l1x
        l2s=pp[16][1]-pp[13][1]
        l2x=pp[13][1]-pp[0][1]
        l2=l2s/l2x
        l3s=pp[12][1]-pp[9][1]
        l3x=pp[9][1]-pp[0][1]
        l3=l3s/l3x
        l4s=pp[8][1]-pp[5][1]
        l4x=pp[5][1]-pp[0][1]
        l4=l4s/l4x
        l5s=pp[4][0]-pp[2][0]
        l5x=pp[2][0]-pp[0][0]
        l5=l5s/l5x
        l1i=int(limitit(l1,1.1,0)*1000+900)
        l2i=int(limitit(l2,1.5,0)*666+950)
        l3i=int(limitit(l3,1.5,0)*666+950)
        l4i=int(limitit(l4,1.2,0)*833+950)
        l5i=int(2000-limitit(l5,0.8,0)*1375)
        print(l1,l2,l3,l4,l5)
        Uart_buf = bytearray([0x55,0x55,0x14, 0x03 ,0x05,0x00,0x01,0x01,l5i & 0x00ff,(l5i  & 0xff00) >>8,0x02,l4i & 0x00ff,(l4i  & 0xff00) >>8,0x03,l3i & 0x00ff,(l3i  & 0xff00) >>8,0x04,l2i & 0x00ff,(l2i  & 0xff00) >>8,0x05,l1i & 0x00ff,(l1i  & 0xff00) >>8 ])
        result=ser.write(Uart_buf)
    cv2.imshow("capture", frame)
    cv2.waitKey(1)
    ed=time.time()
    #print(ed-st)
