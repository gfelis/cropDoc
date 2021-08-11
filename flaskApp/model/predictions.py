from model.utils import *

import pandas as pd

TF_LITE_LABELS = ['rust', 'powdery_mildew', 'frog_eye_leaf_spot', 'complex', 'scab', 'healthy']

def process(img):
    return cv2.resize(img/255.0, (512, 512)).reshape(-1, 512, 512, 3)

def predict_tflite(img, interpreter):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = np.array(process(img), dtype=np.float32)
    
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    
    return get_class(interpreter.get_tensor(output_details[0]['index']), TF_LITE_LABELS)

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

def get_class(prediction: np.ndarray, labels_order: list()):
    classes = pd.Index(labels_order)
    prediction = prediction[0]
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



 

