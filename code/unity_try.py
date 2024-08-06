import cv2
import cvzone.PoseModule
import socket



posefd = cvzone.PoseModule.PoseDetector()

cap = cv2.VideoCapture(0)
cap_w, cap_h = 1280, 720
cap.set(3, cap_w)
cap.set(4, cap_h)

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serveraddressport = ("127.0.0.1", 4990)
while True:
    rt, frame = cap.read()

    frame = posefd.findPose(frame)
    #dst = posefd.findDistance(frame)

    llst , binf = posefd.findPosition(frame, bboxWithHands=False, draw= False)    
    
    data = []

    if llst:
        for ll in llst:
            data.extend([ll[0],cap_h-ll[1],ll[2]])   #unity starting vertices are on bottom right
            conn.sendto(str.encode(str(data)), serveraddressport)

    frame = cv2.flip(frame, 1)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()