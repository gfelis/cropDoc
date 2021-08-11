# Third party libraries
import cv2
import numpy as np
import tensorflow as tf
import os

SHOTS_PATH = "flaskApp/static/shots/"
LABELS_FILE = "labels.csv"

def read_image(image_path: str) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(SHOTS_PATH + image_path), cv2.COLOR_BGR2RGB)
    
def load_model(file_name: str)-> tf.keras.Sequential:
    return tf.keras.models.load_model("flaskApp/model/" + file_name) 

def load_tflite_interpreter(file_name: str):
    return tf.lite.Interpreter(model_path="flaskApp/model/" + file_name)    

def take_picture():
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        cv2.namedWindow("cam-test")
        cv2.imshow("cam-test",img)
        cv2.waitKey(0)
        cv2.destroyWindow("cam-test")
        cv2.imwrite("filename.jpg",img) #save image

def open_labels_csv():
    file_path = os.path.join(SHOTS_PATH, LABELS_FILE)
    if not os.path.exists(file_path):
        f = open(file_path, "w")
        f.write("image_name,labels\n")
        f.close()
    return open(file_path, "a")