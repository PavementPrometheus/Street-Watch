import cv2

from faced import FaceDetector
from faced.utils import annotate_image

face_detector = FaceDetector()

img = cv2.imread(img_path)
rgb_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)

bboxes = face_detector,predict(rgb_img, thresh)

ann_img = annotate_image(img, bboxes)

cv2.imshow('image',ann_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
