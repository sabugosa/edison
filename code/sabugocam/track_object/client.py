# -*- coding: cp1252 -*-
#
#
#
#
#
#

CAMERA_IP_ADDRESS = '10.92.136.73';

import urllib2
import numpy
import cv2
import time
import socket

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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 10666))
while(True):
    img = capture_image()
    data, addr = sock.recvfrom(1024)

    args = data.split(';')

    if len(args) > 0:
        fps = int(args[0])
        x = int(args[1])
        y = int(args[2])
        text1 = "fps          : " + str(fps)
        cv2.line(img,(0,y),(640,y),(0,0,255),3)
        cv2.line(img,(x,0),(x, 480),(0,0,255),3)
    else:
        text = "No data"
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,text1,(10,50), font, 1,(255,255,255),2)

    cv2.imshow('tracking',img)

    #datagram = str(fps) + ";" + str(x) + ";" +str(y) + chr(13)
    #print datagram
    #sock.sendto(datagram, (CLIENT_IP_ADDRESS, 10666))
    if cv2.waitKey(1)& 0xFF == ord(' '):
        break

# When everything done, release the capture
cv2.destroyAllWindows()


