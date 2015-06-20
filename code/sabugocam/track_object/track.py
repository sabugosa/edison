# -*- coding: cp1252 -*-
#
#
#
#
#
#

CAMERA_IP_ADDRESS = '10.92.137.5';

import urllib
#import numpy
import cv2
import datetime

def capture_image(img):
    testfile = urllib.URLopener()
    try:
        testfile.retrieve('http://' + CAMERA_IP_ADDRESS + ':8080/shot.jpg', "shot.jpg")
        img = cv2.imread('shot.jpg')
    except ValueError:
        img = cv2.imread('default.jpg')


while(True):
    img = 0
    capture_image(img)
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


