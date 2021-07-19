from model.utils import *

import pandas as pd

def process(img):
    return cv2.resize(img/255.0, (512, 512)).reshape(-1, 512, 512, 3)

def predict(img, model):
    return model.layers[2](model.layers[1](model.layers[0](process(img)))).numpy()[0]

def find_second_max(list):
    count = 0
    m1 = m2 = float('-inf')
    for x in list:
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1            
            else:
                m2 = x
    return m2 if count >= 2 else None

def find_maximums(list):
    max1, max2, max3= 0, 0, 0	  
    for i in list:	
        if i > max1:	
            max3 = max2 
            max2 = max1 
            max1 = i 
        elif i > max2:	
            max3 = max2 
            max2 = i 
        elif i > max3:	
            max3 = i 
    return max2, max3

def get_class(prediction: np.ndarray):
    classes = pd.Index(['frog_eye_leaf_spot', 'healthy', 'scab', 'complex', 'powdery_mildew', 'rust'])
    percentage = prediction.max()
    class_index = np.where(prediction == percentage)[0][0]
    if percentage <= 0.75:
        second_percentage, third_percentage = find_maximums(prediction)
        if percentage - second_percentage <= 0.25:
            second_index = np.where(prediction == second_percentage)[0][0]
            if second_percentage - third_percentage <= 0.15:
                third_index = np.where(prediction == third_percentage)[0][0]
                return (percentage, second_percentage, third_percentage), classes[class_index] + ' ' + classes[second_index] + ' ' + classes[third_index], prediction
            return (percentage, second_percentage), classes[class_index] + ' ' + classes[second_index], prediction
    return [percentage], classes[class_index], prediction



 

