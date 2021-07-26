from flask import Flask, render_template, Response, request, Blueprint

import model.utils as utils
import model.predictions as pred

import os, datetime

MODEL_FILENAME = "model.h5"

bp = Blueprint('view1', __name__)

model = utils.load_model(MODEL_FILENAME)

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    camera = utils.cv2.VideoCapture(0)

def get_default_photo_name():
    return str(datetime.datetime.now()).replace(";", '')

global capture, switch, photo_name

capture = 0
switch = 1
photo_name = get_default_photo_name()

try:
    os.mkdir('./shots')
except OSError as error:
    pass

def gen_frames():
    global capture, photo_name
    while True:
        success, frame = camera.read() 
        if success:
            if capture:
                capture = 0
                p = os.path.sep.join(['shots', photo_name + ".png"])
                utils.cv2.imwrite(p, frame)
                photo_name = get_default_photo_name()

            try:
                ret, buffer = utils.cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass


@bp.route("/predict")
def predict():
    utils.take_picture()
    image = utils.read_image("test_img.jpg")
    prediction = pred.predict(image, model)
    accuracy, label_predicted, rest = pred.get_class(prediction) #rest of probabilities of classes in rest
    return render_template('pediction.html', label=label_predicted, accuracy=accuracy)

@bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/',methods=['POST','GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture, photo_name
            capture = 1
            photo_name = request.form.get('name')
        elif  request.form.get('stop') == 'Stop/Start':
            
            if switch == 1:
                switch = 0
                camera.release()
                utils.cv2.destroyAllWindows()
            else:
                if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
                    camera = utils.cv2.VideoCapture(0)
                switch = 1
                                     
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')
