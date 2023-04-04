import cv2
import numpy as np

#web camera
cap=cv2.VideoCapture('video.mp4')

min_width_rect=80
min_height_rect=80

count_line_pos =550

algo = cv2.createBackgroundSubtractorKNN()


def center_handle(x,y,w,h):
    x1=int (w/2)
    y1=int (h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect = []
offset=6 #allowable error in the pixel
counter =0

while True:
    ret,frame1=cap.read()
# video ko baar bar chalane k lie loop m
    cv2.imshow('video original',frame1)
    grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(grey,(3,3),5)
    img_sub=algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernal= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernal)
    dilatada = cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernal)
    counterShape,h = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1,(25,count_line_pos),(1200,count_line_pos),(225,127,0),3)
    
    for(i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_rect) and (h>=min_height_rect)
        if not validate_counter:
            continue


        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1,"vehical counter :"+str(counter),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)



        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)


        for(x,y) in detect:
            if y<(count_line_pos+offset)and y>(count_line_pos-offset):
                counter+=1
                cv2.line(frame1,(25,count_line_pos),(1200,count_line_pos),(0,127,255),3)
                detect.remove((x,y))
                print("vehical counter:"+str(counter))


    cv2.putText(frame1,"vehical counter :"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)


    # cv2.imshow('detector',dilatada) this will generATE black and white image running in the background.

# video ko baar bar chalane k lie loop m
    cv2.imshow('video original',frame1)

     #this line tells that when u press enter then it will stop by using waitkey fun
    if cv2.waitKey(1) ==13:
        break


cv2.destroyAllWindows()
cap.release()
#till this line u ca start your web cam



        


