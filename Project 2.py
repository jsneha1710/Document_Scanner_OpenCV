import cv2
import numpy as np
cap=cv2.VideoCapture(1)  #to capture video from webcam (0) and from file(1)
cap.set(3,640) #setting the width and height
cap.set(4,480)
cap.set(10,150)

def preprocessing(img):
    imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur=cv2.GaussianBlur(imggray,(5,5),1)
    imgcanny=cv2.Canny(imgblur,200,200)
    kernel=np.ones(5,5)
    imgdilate=cv2.dilate(imgcanny,kernel,iterations=2)
    imgthres=cv2.erode(imgdilate,kernel,iterations=1)
    return imgthres
def getcontours(img):
    biggest=np.array([])
    maxarea=0
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>5000):
            cv2.drawContours(imgcontour,cnt,-1,(255,0,0),1)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            if(area>maxarea & len(approx)==4):
                biggest=approx
                maxarea=area
    return biggest

def reorder(mypoints):
    mypoints=mypoints.reshape(4,2)
    mypointsnew=np.zeros((4,1,2),np.int32)
    add=mypoints.add(1)
    mypointsnew[0]=mypoints[np.argmin(add)]
    mypointsnew[3] = mypoints[np.argmax(add)]
    diff=mypoints.diff(1)
    mypointsnew[1] = mypoints[np.argmin(diff)]
    mypointsnew[2] = mypoints[np.argmax(diff)]

    return mypointsnew



def getwarp(img,biggest):
    biggest=reorder(biggest)
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[640,0],[0,480],[640,480]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    imgoutput=cv2.warpPerspective(img,matrix,(640,480))

while True:
    success,img=cap.read()
    cv2.resize(img,640,480)
    imgcontour=img.copy()
    Imgthres=preprocessing(img)
    biggest=getcontours(Imgthres)
    getwarp(img,biggest)
    cv2.imshow("Result",Imgthres)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break