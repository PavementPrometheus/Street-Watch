#!/usr/bin/env python2.7
#*****************************************************
# Certain sections of code are from following an online 
# tutorial on OpenCV
# Title: OpenCV Face Recognition
# Author: Adrian Rosebrock
# Date: Sept. 24th, 2018
# Code version: 1.0
# Availability: https://www.pyimagesearch.com
#******************************************************

# Import packages for program
import numpy as np
import argparse
import cv2
import os

# Arguments for command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-f", "--file",
	help="filename of file containing images to test")
args = vars(ap.parse_args())

faces_file = open("faces.txt","r")
line = faces_file.readline()
line = line.split(",")
curr_frame = line[0]
x_value = line[1]
y_value = line[2]
height = line[3]
width = line[4]

print "curr_frame: %s x_value: %s y_value: %s height: %s width: %s" % (curr_frame,x_value,y_value,height,width)

# Load serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#for file in os.listdir(args["file"]):
#    if file.endswith(".jpg"):

#for i in range(0, detections.shape[2]):
# Create blob
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

# Generate detections and predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

# Loop through each detections
for i in range(0, detections.shape[2]):
	confidence = detections[0, 0, i, 2]

	if confidence > args["confidence"]:
		# Generate dimensions for box on face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

                # Create recangle around faces
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
                # Put rectangle on face
		cv2.putText(image, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# Output the facial detection image
cv2.imshow("Output", image)
cv2.waitKey(0)
