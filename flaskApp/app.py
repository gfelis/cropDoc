from flask import Flask, render_template, Response, request

import model.utils as utils
import model.predictions as pred

import os, datetime

MODEL_FILENAME = "model.h5"

app = Flask(__name__)

model = utils.load_model(MODEL_FILENAME)

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    camera = utils.cv2.VideoCapture(0)


global capture, switch

capture = 0
switch = 1

try:
    os.mkdir('./shots')
except OSError as error:
    pass

def gen_frames():
    global capture
    while True:
        success, frame = camera.read() 
        if success:
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                utils.cv2.imwrite(p, frame)

            try:
                ret, buffer = utils.cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass


@app.route("/predict")
def predict():
    utils.take_picture()
    image = utils.read_image("test_img.jpg")
    prediction = pred.predict(image, model)
    accuracy, label_predicted, rest = pred.get_class(prediction) #rest of probabilities of classes in rest
    return render_template('index.html', label=label_predicted, accuracy=accuracy)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera')
def take_picture():
    return render_template('camera.html')

@app.route('/',methods=['POST','GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
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
        return render_template('cafe.html')
    return render_template('cafe.html')

if __name__ == '__main__':
    app.run(debug=True)
