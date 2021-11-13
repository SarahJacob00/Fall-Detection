from keypoints import get_keypoints
from parseout import parse_output,draw_kps,draw_deviations,draw_skeleton
import cv2
import matplotlib.pyplot as plt
import numpy as np


#TESTING A FRAME OF VIDEO
def model(video):
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    frame_height, frame_width, _ = frame.shape
    #print("Processing Video...")


    hip=[]
    head=[]
    foot=[]
    bound_box=[]
    i=0
    count=0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            #out.release()
            break

        i=i+1
        template_show,template_kps,height,width=get_keypoints(frame,i)

        #----------------------------------------------FILTERING------------------------------------------------
        error=0
        for x in range (0,len(template_kps)-1):
            #---------------x coord----------------------
            m=template_kps[x][0]
            n=template_kps[x+1][0]
            if(n>m):
                m,n=n,m

            if(abs(m-n)>(width/2.5)):
              #print("diff x: ",m-n)
              error=1

            #-----------y coord----------------------
            m=template_kps[x][1]
            n=template_kps[x+1][1]
            if(n>m):
                m,n=n,m

            if(abs(m-n)>(height/2.5)):
              #print("diff y: ",m-n)
              error=1


        #print("error=.",error)
        if(error==1):
            continue

        count=count+1
        out_frame,h,w=draw_skeleton(template_show, template_kps)
        i=i+1
        #--------------------------------------- HIPPOINT PARAMETER 1:VELOCITY-----------------------------------------------
        x1 = template_kps[6][0]  #LEFT HIP
        y1 = template_kps[6][1]
        x2 = template_kps[7][0] #RIGHT HIP
        y2 = template_kps[7][1]

        xm=(x2+x1)/2
        ym=(y2+y1)/2

        hip.append([i,ym])          # store value of y coordinate in list to compare two frames



        #---------------------------------------------HEAD, LEGS PARAMETER 2:ANGLE--------------------------------------------
        x5 = template_kps[0][0] #LEFT SHOULDER
        y5 = template_kps[0][1]
        x6 = template_kps[1][0] #RIGHT SHOULDER
        y6 = template_kps[1][1]

        xm2=(x5+x6)/2
        ym2=(y5+y6)/2

        head.append([i,xm2,ym2])

        x9 = template_kps[10][0] #LEFT FOOT
        y9 = template_kps[10][1]
        x4 = template_kps[11][0] #RIGHT FOOT
        y4 = template_kps[11][1]

        xm1=(x9+x4)/2
        ym1=(y9+y4)/2


        foot.append([i,xm1,ym1])

        #--------------------------------------------BOUNDING BOX PARAMETER 3-------------------------------------------------

        ratio=w/h

        if(h>=w):state=1
        else:state=-1
        #print('STATE,W,H=',state,w,h)
        bound_box.append([i,ratio,state,w,h])


    #----------------------------------------------PRINT TIMEFRAMES    
        #i=i+1
        #print('Timeframe=',i)
        #plt.imshow(out_frame)
        #plt.show()

    #print('NO OF FRAMES', count)
    fall=0
    vel_angle=[]
    
    #--------------------------CHECKINGGGG------------------------------------------------------------------
    
    
    str_fall=""
    str_stood=""
    
    for i in range(0,len(hip)-3):
        stood=0
        if fall==1:break
    
        counter=[]
        #print('in11')
        if((i+5)>=len(hip)):break
        
        
        #1. VELOCITY
        v=(abs(hip[i+3][1]-hip[i][1])/3)   
       
    
          #2. ANGLE
        a = np.array([head[i][1],head[i][2]])
        b = np.array([foot[i][1],foot[i][2]])
        c = np.array([head[i+3][1],head[i+3][2]])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        #print()
        vel_angle.append([hip[i][0],v,np.degrees(angle)])    

       

        if (v > 25 and np.degrees(angle)>50 or bound_box[i][2]==-1):#and 
        
            fall=1
           
            #print("FALL DETECTED AT :",hip[i][0])
            str_fall="FALL DETECTED"

            if bound_box[i][1]>1:
                #print('BOUNDING BOX')
                #print('State,w,h=',bound_box[i][2],bound_box[i][3],bound_box[i][4])
                stood=0
                #fall=1
                box=0
                if i+30>len(hip):l=len(hip)
                else: l=i+30
                for j in range(i,l):
                    if bound_box[j][1]<1:
                        box=box+1
                if box>24:
                    stood=1
            else:    
                #print('SPEED')
                for j in range(i+10,i+20):
                    #print('j=',j)
                    a = np.array([head[j][1],head[j][2]])
                    b = np.array([foot[j][1],foot[j][2]])
                    c = np.array([head[j+3][1],head[j+3][2]])

                    ba = a - b
                    bc = c - b

                    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                    angle2 = np.arccos(cosine_angle)


                    #print('angle2=',np.degrees(angle2))
                    if (np.degrees(angle2)>10):
                        #print('ANGLE STOOD UP AT:',np.degrees(angle2))
                        #print("PERSON HAS STOOD UP",hip[j][0])
                        stood=1
                        break
                if stood==1:break

    if fall==0: str_fall="NO FALL"   #print(' NO FALL ')       
    elif stood==0:str_stood="PERSON HAS NOT STOOD UP"  #print("PERSON HAS NOT STOOD UP",hip[i][0])
    else :str_stood="PERSON HAS STOOD UP"    #print("PERSON HAS STOOD UP",hip[i][0])
       
    return str_fall,str_stood,stood,fall
    #print("Done processing video")