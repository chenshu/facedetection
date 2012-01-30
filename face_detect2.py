#!/usr/bin/python
# -*- coding: UTF-8 -*-

# face_detect.py

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

# Usage: python face_detect.py <image_file>

import sys, os
from opencv.cv import *
from opencv.highgui import *
from PIL import Image, ImageDraw
from math import sqrt

def detectObjects(image):
    """Converts an image to grayscale and prints the locations of any faces found"""
    grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
    cvCvtColor(image, grayscale, CV_BGR2GRAY)

    storage = cvCreateMemStorage(0)
    cvClearMemStorage(storage)
    cvEqualizeHist(grayscale, grayscale)
    cascade = cvLoadHaarClassifierCascade('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml', cvSize(1,1))
    #faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.1, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(20,20))
    faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))

    result = []
    for f in faces:
        result.append((f.x, f.y, f.x+f.width, f.y+f.height))

    print result
    return result

def grayscale(r, g, b):
    return int(r * .3 + g * .59 + b * .11)

def process(infile, outfile):

    image = cvLoadImage(infile);
    if image:
        faces = detectObjects(image)

    im = Image.open(infile)

    if faces:
        draw = ImageDraw.Draw(im)
        for f in faces:
            draw.rectangle(f, outline=(255, 0, 255))

        im.save(outfile, "JPEG", quality=100)
    else:
        print "Error: cannot detect faces on %s" % infile

if __name__ == "__main__":
    process(sys.argv[1], 'output.jpg')
