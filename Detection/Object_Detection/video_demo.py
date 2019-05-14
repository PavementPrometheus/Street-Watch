from __future__ import division
import time
import torch 
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2 
from util import *
from darknet import Darknet
from preprocess import prep_image, inp_to_image, letterbox_image
import pandas as pd
import random 
import pickle as pkl
import argparse
import time
import datetime
import os
import requests
import imutils
from imutils.video import VideoStream

tout = 1.5
faceFile = 'pedloc.txt'
streetapiurl = 'http://192.168.99.100:4000/pavement'
cameraNum = '123'
location = 'Intersection of 1234 fake st. and 5th fabricated blvd.'

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

#Face detection
def face_detect(image, num_faces_detected):
    #cv2.imwrite("original_img.jpg",image)    
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
       (300, 300), (104.0, 177.0, 123.0))
#    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    #If face not detected, obscure pedestrian
#    if len(detections) == 0:
#        startY = y_value - 0.5*height
#        startX = x_value = 0.5*width
#        endY = startY + height
#        endX = startX + width
#        image = cv2.rectangle(image, (startX, startY), (endX, endY),
#            (0, 0, 255), 2)
#        person = image[startY:endY, startX:endX]
        # Blur the pedestrian image
#        person = cv2.GaussianBlur(person, (73, 73), 30)
        # Put the pedestrian region back into the frame image
#        image[startY:endY, startX:endX] = person

#        print("Face not detected")
        #cv2.imshow("Output", image)
        #cv2.waitKey(0)

    # Go through every detected face within the image
    #print("detections: ",len(detections))
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.3:
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
            
            #Blur the face image
            face = cv2.GaussianBlur(face, (73, 73), 30)
            num_faces_detected += 1
            # Put the blurred face region back into the frame image
            image[startY:endY, startX:endX] = face
    #cv2.imshow("Output", image)
#    filestream.close()
    #cv2.imwrite("output_img.jpg",image)    
    return image


#Pedestrian detection
def get_test_input(input_dim, CUDA):
    img = cv2.imread("dog-cycle-car.png")
    img = cv2.resize(img, (input_dim, input_dim)) 
    img_ =  img[:,:,::-1].transpose((2,0,1))
    img_ = img_[np.newaxis,:,:,:]/255.0
    img_ = torch.from_numpy(img_).float()
    img_ = Variable(img_)
    
    if CUDA:
        img_ = img_.cuda()
    
    return img_

def prep_image(img, inp_dim):
    """
    Prepare image for inputting to the neural network. 
    
    Returns a Variable 
    """

    orig_im = img
    dim = orig_im.shape[1], orig_im.shape[0]
    img = (letterbox_image(orig_im, (inp_dim, inp_dim)))
    img_ = img[:,:,::-1].transpose((2,0,1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, orig_im, dim
    
def send_request(data):
    url =  streetapiurl
    try:
        requests.post(url = url, data = data, timeout=tout)
    except requests.Timeout:
        pass
    except requests.ConnectionError:
        print("Error: Not finding database")

def write(x, img, fr, curdate):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    cls = int(x[-1])
    
    if(cls == 0):
        x1 = int(c1[0])
        x2 = int(c2[0])
        y1 = int(c1[1])
        y2 = int(c2[1])
        width = x2-x1
        height = y2-y1
        centerx = x2 - (width/2)
        centery = y2 - (height/2)
        if os.path.exists(os.path.join('output', faceFile)):
            wr = 'a'
        else:
            wr = 'w'
        file = open(os.path.join('output', faceFile), wr)
        file.write(str(fr) + "," + str(centerx) + "," + str(centery) + "," + str(width) + "," + str(height) + "\n")
        file.close()
    
    if(cls == 2):
        #label = "{0}".format(classes[cls])
        #color = random.choice(colors)
        #if((c2[0]-c1[0]) < 850):
        #    cv2.rectangle(img, c1, c2,color, -1)
        #cv2.rectangle(img, c1, c2,color, 1)
        #t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
        #c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        #cv2.rectangle(img, c1, c2,color, -1)
        #cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1)
    return img

def arg_parse():
    """
    Parse arguements to the detect module
    
    """
    
    
    parser = argparse.ArgumentParser(description='YOLO v3 Video Detection Module')
   
    parser.add_argument("--video", dest = 'video', help = 
                        "Video to run detection upon",
                        default = "video.avi", type = str)
    parser.add_argument("--dataset", dest = "dataset", help = "Dataset on which the network has been trained", default = "pascal")
    parser.add_argument("--confidence", dest = "confidence", help = "Object Confidence to filter predictions", default = 0.5)
    parser.add_argument("--nms_thresh", dest = "nms_thresh", help = "NMS Threshhold", default = 0.4)
    parser.add_argument("--cfg", dest = 'cfgfile', help = 
                        "Config file",
                        default = "cfg/yolov3.cfg", type = str)
    parser.add_argument("--weights", dest = 'weightsfile', help = 
                        "weightsfile",
                        default = "yolov3.weights", type = str)
    parser.add_argument("--reso", dest = 'reso', help = 
                        "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                        default = "416", type = str)
    parser.add_argument("--output", dest = 'output', help =
                        "video output dir",
                        default = "output", type = str)
    parser.add_argument("--noshow", dest = 'noshow', help =
                        "wether show frame",
                        default = False, type = bool)
    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()
    confidence = float(args.confidence)
    nms_thesh = float(args.nms_thresh)
    start = 0

    CUDA = torch.cuda.is_available()

    num_classes = 80

    CUDA = torch.cuda.is_available()
    
    bbox_attrs = 5 + num_classes
    
    print("Loading network.....")
    model = Darknet(args.cfgfile)
    model.load_weights(args.weightsfile)
    print("Network successfully loaded")

    model.net_info["height"] = args.reso
    inp_dim = int(model.net_info["height"])
    assert inp_dim % 32 == 0 
    assert inp_dim > 32

    if CUDA:
        model.cuda()
        
    model(get_test_input(inp_dim, CUDA), CUDA)

    model.eval()
    
    videofile = args.video
    #Video from file
    cap = cv2.VideoCapture(videofile)
    #Video stream from webcam
    #cap = VideoStream(src=0).start()
    #time.sleep(2.0)
    #cap = VideoStream(src=0).start()

    FRAME_WIDTH = cap.get(3)
    FRAME_HEIGHT = cap.get(4)
    FRAME_FPS = cap.get(5)
    FRAME_FOURCC = cap.get(6)
    FRAME_FOURCC_1 = cap.get(cv2.CAP_PROP_FOURCC)
    print (FRAME_WIDTH, FRAME_HEIGHT, FRAME_FPS, FRAME_FOURCC, FRAME_FOURCC_1)
    output_file = args.output + '\\result_' +args.video.split('\\')[-1]
    print(output_file)
    out = cv2.VideoWriter(output_file, int(FRAME_FOURCC), FRAME_FPS, (int(FRAME_WIDTH),int(FRAME_HEIGHT)))
    assert cap.isOpened(), 'Cannot capture source'
    
    try:
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'frames'))
    except FileExistsError:
        pass
    
    frames = 0
    start = time.time()
    start_time = time.time()    
    while cap.isOpened():

        #face_detect_video(videofile)

        ret, frame = cap.read()
        if ret:

            data = {}
            #frame = face_detect(frame)
            img, orig_im, dim = prep_image(frame, inp_dim)

            im_dim = torch.FloatTensor(dim).repeat(1,2)                        
            
            
            if CUDA:
                im_dim = im_dim.cuda()
                img = img.cuda()
            
            with torch.no_grad():   
                output = model(Variable(img), CUDA)
            output = write_results(output, confidence, num_classes, nms = True, nms_conf = nms_thesh)
            #orig_im = face_detect(orig_im)
            #print("you made it out of face detection")
            
            if type(output) == int:
                frames += 1
                # print("FPS of the video is {:5.2f}".format( frames / (time.time() - start)))
                # print('============================================================')
                if not args.noshow:
                    cv2.imshow("frame", orig_im)
                if args.output is not None:
                    out.write(orig_im)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                continue
            
            im_dim = im_dim.repeat(output.size(0), 1)
            scaling_factor = torch.min(inp_dim/im_dim,1)[0].view(-1,1)
            
            output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim[:,0].view(-1,1))/2
            output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim[:,1].view(-1,1))/2
            
            output[:,1:5] /= scaling_factor
    
            for i in range(output.shape[0]):
                output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim[i,0])
                output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim[i,1])
            
            classes = load_classes('data/coco.names')
            colors = pkl.load(open("pallete", "rb"))

            counts = list(map(lambda y: int(y[-1]), output))
            str1 = "People: "
            str2 = "Cars: "
            num1 = counts.count(0)
            num2 = counts.count(2)
            cv2.rectangle(orig_im, (10,20), (200,120), (0, 0, 0), -1)
            cv2.putText(orig_im, str1+str(num1), (20,55), cv2.FONT_HERSHEY_PLAIN, 2, [225,255,255], 1);
            cv2.putText(orig_im, str2+str(num2), (20,95), cv2.FONT_HERSHEY_PLAIN, 2, [225,255,255], 1);
            
            num_faces_detected = 0
            orig_im = face_detect(orig_im, num_faces_detected)
            print("num_faces_detected",num_faces_detected)
#            print("YOU ARE HERE")
            
            #curdate = int(round(time.time() * 1000))
            curdate = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            data = {
                'date': curdate,
                'frame': frame,
                'cameraNum': cameraNum,
                'peopleSum': num1,
                'carSum': num2
            }
            
            #send_request(data)
            
            list(map(lambda x: write(x, orig_im, frames, curdate), output))
            
            name = cameraNum + "_" + str(frames) + ".jpg"
            cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'frames', name), orig_im)
            
            cv2.imshow("frame", orig_im)
            if not args.noshow:
                    cv2.imshow("frame", orig_im)
            if args.output is not None:
                    out.write(orig_im)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            frames += 1
            #print("FPS of the video is {:5.2f}".format( frames / (time.time() - start)))

            
        else:
            break
    # fourcc = cv2.writer (*'XVID')
    cap.release()
    out.release()
    end_time = time.time()
    print ("time: {}".format(str(end_time-start_time)))
    

    
    

