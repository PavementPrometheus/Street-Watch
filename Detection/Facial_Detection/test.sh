#!/bin/bash

#Detect faces
#python detect_faces.py --image michael_scott.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image seniors.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image texting.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image hipsters.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

#Blur faces
#python blur_faces.py --image michael_scott.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image seniors.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image texting.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image hipsters.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python blur_faces.py --image original_img.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
