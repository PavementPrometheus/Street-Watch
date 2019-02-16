# Facial Detection

### Goal 
By detecting and obfuscating faces of pedestrians, our group can retain important data while protecting the identities of pedestrians.

This program uses OpenCV features to detect and obfuscate faces, so please ensure requirements are installed before run.  
**detect_faces.py** - Detects the faces of pedestrians and outputs the confidence  
**blur_faces.py** - Detects the faces of pedestrians and outputs the confidence and obfuscated (blurred) faces

### Program execution options:
**1) Run test.sh** - this is a demo script that will take in pre-selected images and output them, running both detect_faces.py and blur_faces.py  
**2) Run the following command:**  
```python <py_file_name> --image <image_name> --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel```

**Example:**  
```python detect_faces.py --image michael_scott.jpg --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel```

**<py_file_name>** : either detect_faces.py or blur_faces.py  
**<image_name>** : name of image to be used

**Example output:**   
After running the previous command, example output would be:   
**original image** &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; **detect_faces.py:** &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; **blur_faces.py**     
<img src="https://github.com/PavementPrometheus/Street-Watch/blob/master/Facial_Detection/michael_scott.jpg" width="30%">
<img src="https://github.com/PavementPrometheus/Street-Watch/blob/master/Facial_Detection/output/michael_detect.JPG" width="30%">
<img src="https://github.com/PavementPrometheus/Street-Watch/blob/master/Facial_Detection/output/michael_blur.JPG" width="30%">
