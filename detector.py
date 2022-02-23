import cv2,os,mysql.connector
import numpy as np
from PIL import Image 
import pickle
#face detection code
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cam = cv2.VideoCapture(0)
key=1
while key==1:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        if(nbr_predicted==5):
            print('Student Match Found.Student ID is:')
            print(nbr_predicted)
        else:
            print('Match not found')
        cv2.imshow('im',im)
        cv2.waitKey(10)
        key=0
        
#database code
nbr_predicted=(str(nbr_predicted),)
conn=mysql.connector.connect(user='root',password='root',host='localhost',database='project')
cursor=conn.cursor()
cursor.execute ("""
   UPDATE attendance
   SET classes=classes+1
   WHERE id=%s
""", (nbr_predicted))
conn.commit()
conn.close()
