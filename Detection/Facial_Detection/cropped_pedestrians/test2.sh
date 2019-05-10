#!/bin/bash

#Detect faces
python detect_faces.py --image michael_scott.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image seniors.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image texting.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image hipsters.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

#Cropped Images
python detect_faces.py --image "0.png" --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image "210.png" --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image "270.png" --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python detect_faces.py --image "360.png" --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

#python detect_faces.py --image 0_0_x1-625_x2-661_y1-288_y2-378.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image 0_210_x1-630_x2-741_y1-184_y2-479.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image 0_270_x1-0_x2-312_y1-171_y2-690.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python detect_faces.py --image 0_360_x1-20_x2-634_y1-7_y2-690.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel


#Blur faces
python blur_faces.py --image michael_scott.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python blur_faces.py --image seniors.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python blur_faces.py --image texting.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
python blur_faces.py --image hipsters.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

#Cropped Images
#python blur_faces.py --image 0.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 210.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 270.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 360.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

#python blur_faces.py --image 0_0_x1-625_x2-661_y1-288_y2-378.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 0_210_x1-630_x2-741_y1-184_y2-479.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 0_270_x1-0_x2-312_y1-171_y2-690.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
#python blur_faces.py --image 0_360_x1-20_x2-634_y1-7_y2-690.png --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
