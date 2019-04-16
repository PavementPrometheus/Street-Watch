#*****************************************************
# Certain sections of code are from following an online 
# tutorial on OpenCV
# Title: OpenCV Face Recognition
# Author: Adrian Rosebrock
# Date: Sept. 24th, 2018
# Code version: 1.0
# Availability: https://www.pyimagesearch.com
#******************************************************

# Import needed packages
import numpy as np
import argparse
import cv2

# Generate command line arguments
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

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Create blob image to be used
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

# Go through every detected face within the image
for i in range(0, detections.shape[2]):
	confidence = detections[0, 0, i, 2]

	if confidence > args["confidence"]:
		# Generate the box around the people's faces
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
                
                # Put the rectangle around the person's face
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		image = cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		cv2.putText(image, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		face = image[startY:endY, startX:endX]
		# Blur the face image
		face = cv2.GaussianBlur(face, (73, 73), 30)
		# Put the blurred face region back into the frame image
		image[startY:endY, startX:endX] = face

# Output the resulting obscurred image to the user
cv2.imshow("Output", image)
cv2.waitKey(0)
