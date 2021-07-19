# Third party libraries
import cv2
import numpy as np
import tensorflow as tf


def read_image(image_path: str) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    
def load_model(file_name: str)-> tf.keras.Sequential:
    return tf.keras.models.load_model("flaskApp/model/" + file_name) 


def take_picture():
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        cv2.namedWindow("cam-test")
        cv2.imshow("cam-test",img)
        cv2.waitKey(0)
        cv2.destroyWindow("cam-test")
        cv2.imwrite("filename.jpg",img) #save image
