import numpy as np
import cv2
import time

dist = 0
focal = 1300
pixels = 30
width = 5

def get_dist(rectange_params,image):
    pixels = rectange_params[1][0]
    print(pixels)

    dist = (width*focal)/pixels

    image = cv2.putText(image, 'Distance from Camera (CM)', org, font,
       1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(dist), (150,70), font,
       fontScale, color, 1, cv2.LINE_AA)

    jarak = int(round(180-dist))
    step = round(jarak/76)
    if (dist<180):
        image = cv2.putText(image, 'WARNING CORONA!!!!', (10,250), font,
           2, (0, 0, 255), 3, cv2.LINE_AA)
        image = cv2.putText(image, 'RUNN!!!!', (200,300), font,
           2, (0, 0, 255), 3, cv2.LINE_AA)
        image = cv2.putText(image, 'step back' + str(jarak) + 'cm', (200,350), font,
           0.7, (0, 0, 255), 1, cv2.LINE_AA)
        image = cv2.putText(image, 'step back' + str(step) + 'step', (200,380), font,
           1, (0, 255, 255), 1, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'SAVE', (200,300), font,
           2, (0, 255, 0), 3, cv2.LINE_AA)
    return image

cap = cv2.VideoCapture(0)

kernel = np.ones((3,3),'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX
org = (100,50)
fontScale = 0.8
color = (0, 0, 0)
thickness = 2


cv2.namedWindow('DONT GET TO CLOSE ',cv2.WINDOW_NORMAL)
cv2.resizeWindow('DONT GET TO CLOSE ', 700,600)


while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


    lower = np.array([0, 39, 18])
    upper = np.array([13, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)



    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)


    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont:
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)

            img = get_dist(rect,img)

    cv2.imshow('DONT GET TO CLOSE ',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
