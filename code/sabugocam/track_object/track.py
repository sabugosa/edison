# -*- coding: cp1252 -*-
#
#
#
#
#
#

CAMERA_IP_ADDRESS = '10.92.136.73';
CLIENT_IP_ADDRESS = '10.92.137.18';

DEBUG = False

import urllib2
import numpy
import cv2
import time
import socket

angx = 90
angy = 90

def capture_image():

    #testfile = urllib.URLopener()
    try:
        #testfile.retrieve('http://' + CAMERA_IP_ADDRESS + ':8080/shot.jpg', "shot.jpg", timeout=1)
        #img = cv2.imread('shot.jpg')
        u = urllib2.urlopen('http://' + CAMERA_IP_ADDRESS + ':8080/shot.jpg')
        secs = time.time()

        f = open('shot.jpg', 'wb')
        meta = u.info()
        if len(meta.getheaders("Content-Length")) == 0:
            img = cv2.imread('default.jpg')
            return img

        file_size = int(meta.getheaders("Content-Length")[0])
        #print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        error = False
        while True:
            if (time.time() - secs) > 1:
                error = True
                break

            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            #status = status + chr(8)*(len(status)+1)
            #print status,
        f.close()
        if error:
            img = cv2.imread('default.jpg')
            print "timeout: " + str(time.time() - secs)
        else:
            img = cv2.imread('shot.jpg')

    except IOError:
        img = cv2.imread('default.jpg')
    return img

def track(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgT = cv2.inRange(imgHSV, (iLowH, iLowS, iLowV), (iHighH, iHighS, iHighV))

    kernel = numpy.ones((15,15),numpy.uint8)
    imgT = cv2.erode(imgT, kernel, iterations = 1)
    imgT = cv2.dilate(imgT, kernel,iterations = 1)

    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 10

    # Filter by Circularity
    params.filterByCircularity = False #True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False # True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False # True
    params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector(params)

    keypoints = detector.detect(imgT)
    #im_with_keypoints = cv2.drawKeypoints(imgT, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    posX = -1
    posY = -1
    dArea=0
    #print "size: " + str(len(keypoints))
    count = 0
    posX = 0
    posY = 0
    for kp in keypoints:
        area = kp.size
        #print area
        if area > dArea and area > 2:
            count = count + 1
            x,y = kp.pt
            posX = posX + int(x)
            posY = posY + int(y)
            dArea = area
    if (count > 0):
        posX = int(float(posX)/ float(count))
        posY = int(float(posY)/ float(count))

        cv2.line(imgT,(0,posY),(640,posY),(255,0,0),1)
        cv2.line(imgT,(posX,0),(posX, 480),(255,0,0),1)
    else:
        posX = -1
        posY = -1
    if DEBUG:
        cv2.imshow('processed image',imgT)
    return (posX, posY)

def commandPanAndTilt(x,y):
    global angx
    global angy

    ax = x * 180 / 480;
    ay = y * 180 / 480;

    #print "ax=",ax,", ay=",ay

    if (ay > 45 ) and (ay < 135):
        ay = angy
    else:
        angy = ay
    if (ax > 45 ) and (ax < 135):
        ax = angx
    else:
        angx = ax

    url ="http://127.0.0.1?joy=0"
    url = url + "&x=" + str(angx)
    url = url + "&y=" + str(angy)

    print url

    try:
        u = urllib2.urlopen(url + "8000")
    except IOError:
        print "failed to send pan and tilt command"

def nothing(x):
    pass

iLowH = 22
iHighH = 98
iLowS = 0
iHighS = 255
iLowV = 0
iHighV = 254

if DEBUG:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # create trackbars for color change
    cv2.createTrackbar('LowH','image',0,255,nothing)
    cv2.createTrackbar('HighH','image',0,255,nothing)
    cv2.createTrackbar('LowS','image',0,255,nothing)
    cv2.createTrackbar('HighS','image',0,255,nothing)
    cv2.createTrackbar('LowV','image',0,255,nothing)
    cv2.createTrackbar('HighV','image',0,255,nothing)

    cv2.setTrackbarPos('LowH','image', iLowH)
    cv2.setTrackbarPos('HighH','image', iHighH)
    cv2.setTrackbarPos('LowS','image', iLowS)
    cv2.setTrackbarPos('HighS','image', iHighS)
    cv2.setTrackbarPos('LowV','image', iLowV)
    cv2.setTrackbarPos('HighV','image', iHighV)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while(True):
    millis = int(round(time.time() * 1000))

    if DEBUG:
        iLowH = cv2.getTrackbarPos('LowH','image')
        iHighH = cv2.getTrackbarPos('HighH','image')
        iLowS = cv2.getTrackbarPos('LowS','image')
        iHighS = cv2.getTrackbarPos('HighS','image')
        iLowV = cv2.getTrackbarPos('LowV','image')
        iHighV = cv2.getTrackbarPos('HighV','image')

    img = capture_image()
    time1 = int(round(time.time() * 1000)) - millis

    millis2 = int(round(time.time() * 1000))
    x,y = track(img)

    if x >= 0:
        commandPanAndTilt(x,y)
    time2 = int(round(time.time() * 1000)) - millis2

    cv2.line(img,(0,y),(640,y),(255,0,0),1)
    cv2.line(img,(x,0),(x, 480),(255,0,0),1)
    fps = 1000/(time1 + time2)
    text1 = "time capture : " + str(time1)
    text2 = "time track   : " + str(time2)
    text3 = "fps          : " + str(fps)
    text4 = "object pos   : " + str(x) + ", " + str(y)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,text1,(10,50), font, 1,(255,255,255),2)
    cv2.putText(img,text2,(10,80), font, 1,(255,255,255),2)
    cv2.putText(img,text3,(10,110), font, 1,(255,255,255),2)
    cv2.putText(img,text4,(10,140), font, 1,(255,255,255),2)

    if DEBUG:
        cv2.imshow('phone image',img)

    datagram = str(fps) + ";" + str(x) + ";" +str(y) + chr(13)
    print datagram
    sock.sendto(datagram, (CLIENT_IP_ADDRESS, 10666))
    if cv2.waitKey(1)& 0xFF == ord(' '):
        break

# When everything done, release the capture
cv2.destroyAllWindows()


