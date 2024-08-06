import cv2
import os
from matplotlib.patches import draw_bbox
import mediapipe
import cvzone.PoseModule

def img_crp(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cn = cv2.Canny(gray, 20, 255)
    thresh = cv2.threshold(cn, 20, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    #cv2.drawContours(image,cnts,-1,(0,255,0),1) 
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+w]
        
        break
    return ROI 

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1000)
rt, frame = cap.read()
h,w,ch = frame.shape

shirt_dir = "C:\\Vrishank\\virtual_trial_room\\shirts_img"
l_shirt = os.listdir(shirt_dir)
shirt_no = 0

#print(l_shirt)
# 500 * 500 pixel image was used for the shirt
#shirt = cv2.imread("C:\\Vrishank\\virtual_trial_room\\shirts_img\\black_shirt_front_nobg.png", cv2.IMREAD_UNCHANGED)
#h1,w1,ch1 = shirt.shape
#img_ratio = int(h1/w1)

pant_dir = "C:\\Vrishank\\virtual_trial_room\\pants_img"
l_pant = os.listdir(pant_dir)
pant_no = 1
#print(l_pant)
# 484 * 1098 pixel image was used for the pants
#pant = cv2.imread("C:\\Vrishank\\virtual_trial_room\\pants_img\\blue_pant_front_trimmed.png", cv2.IMREAD_UNCHANGED)
#h2,w2,ch2 = pant.shape
#img_ratio = int(h2/w2)

sz="XL"
font_scale = 0.5
counter = 0
speed_e = 10

posefd = cvzone.PoseModule.PoseDetector()

while True:
    rt, frame = cap.read()
    frame = posefd.findPose(frame)
    #dst = posefd.findDistance(frame)

    llst , binf = posefd.findPosition(frame, bboxWithHands=False, draw= False)    #this part is code is common for all
    if llst:
        pt11 = llst[11]                 #co-ordinates for shoulder
        pt12 = llst[12]                 #co-ordinates for shoulder 
        pt24 = llst[24]                 #co-ordinates for hip 
        pt23 = llst[23]                 #co-ordinates for hip
        pt27 = llst[27]                 #co-ordinates for ankle


        shirt = cv2.imread(os.path.join(shirt_dir,l_shirt[shirt_no]), cv2.IMREAD_UNCHANGED)
        #shirt = img_crp(shirt)
        h1,w1,ch1 = shirt.shape
        img_ratio = int(h1/w1)


        pant = cv2.imread(os.path.join(pant_dir,l_pant[pant_no]), cv2.IMREAD_UNCHANGED)
        #pant = img_crp(pant)
        h2,w2,ch2 = pant.shape
        img_ratio = int(h2/w2)


        #------------------------------------------------------------------
        # shirt and pant change
        if ((llst[15][0] > pt11[0]) and (llst[16][0] > pt11[0])):
            #shirt change to next
            #top left region
            if (llst[15][1] < (h/2)) and (llst[16][1] < (h/2)):
                counter += 1
                cv2.ellipse(frame, (int((3*w)/4), int(h/4)), (66,66), 0, 0, counter*speed_e, (0,255,0), 20)
                if counter * speed_e > 360:
                    counter = 0
                    if(shirt_no < len(l_shirt)-1):
                        shirt_no += 1
            #pant change to next
            #bottom teft region
            elif (llst[15][1] > (h/2)) and (llst[16][1] > (h/2)):
                counter += 1
                cv2.ellipse(frame, (int((3*w)/4), int((3*h)/4)), (66,66), 0, 0, counter*speed_e, (0,255,0), 20)
                if counter * speed_e > 360:
                    counter = 0
                    if(pant_no < len(l_pant)-1):
                        pant_no += 1


        elif((llst[15][0] < pt12[0]) and (llst[16][0] < pt12[0])):
            #shirt change to prev
            #top right region
            if (llst[15][1] < (h/2)) and (llst[16][1] < (h/2)):
                counter += 1
                cv2.ellipse(frame, (int(w/4), int(h/4)), (66,66), 0, 0, counter*speed_e, (0,255,0), 20)
                if counter * speed_e > 360:
                    counter = 0
                    if(shirt_no > 0):
                        shirt_no -= 1
            #pant change to prev
            #bottom left region
            elif (llst[15][1] > (h/2)) and (llst[16][1] > (h/2) and pant_no > 0):
                counter += 1
                cv2.ellipse(frame, (int(w/4), int((3*h)/4)), (66,66), 0, 0, counter*speed_e, (0,255,0), 20)
                if counter * speed_e > 360:
                    counter = 0
                    if(pant_no > 0):
                        pant_no -= 1



        
        s_width = int((pt11[0] - pt12[0])*1.9)                #shirt width
        s_height = int((pt24[1] - pt12[1])*1.4)               #shirt height
        p_width = int((pt23[0] - pt24[0])*2)                #pant width
        p_height = int((pt27[1] - pt23[1])*1.5)             #pants height


        s_offset_ratio = (pt11[0] - pt12[0])/w1            #offset ratio of shirt
        s_offset = [int(200 * s_offset_ratio), int(150 * s_offset_ratio)]       #values should be changed if shirt image dimensions change

        try:
            s_ROI = cv2.resize(shirt , (s_width, s_height))         #shirt resize
            cv2.imshow("shirt", s_ROI)
        except:
            print("Resizing")

        try:
            cvzone.overlayPNG(frame, s_ROI, pos=(pt12[0]-s_offset[0], pt12[1]-s_offset[1]))     #shirt overlay
        except:
            print("Overlay error, recalculating... ")

#------------------------------------------------------------------------------------------------------------------------
#pant section
        p_offset_ratio = (pt23[0] - pt24[0])/w2            #offset ratio of pant
        p_offset = [int(240 * p_offset_ratio), int(250 * p_offset_ratio)]
        #print(p_offset[0],"   |||   ",p_offset[1])
        try:
            p_ROI = cv2.resize(pant , (p_width, p_height))         #pant resize
            cv2.imshow("pant", p_ROI)
        except:
            print("Resizing")

        try:
            cvzone.overlayPNG(frame, p_ROI, pos=(pt24[0]-p_offset[0], pt24[1]-p_offset[1]))     #pant overlay
        except:
            print("Overlay error, recalculating... ")


        
    cv2.imshow("frame", frame)
    
    cv2.waitKey(1)


cv2.destroyAllWindows()
cap.release()



