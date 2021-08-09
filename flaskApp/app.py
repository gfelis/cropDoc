from flask import Flask, render_template, Response, request
from flask.helpers import make_response
from flask_cors import CORS, cross_origin

import model.utils as utils
import model.predictions as pred

import os, time

# MODEL_FILENAME = "model.h5"
MODEL_TFLITE = "model.tflite"
IMG_FOLDER = "flaskApp/static/shots"

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})

# model = utils.load_tflite_model(MODEL_FILENAME)
interpreter = utils.load_tflite_interpreter(MODEL_TFLITE)
interpreter.allocate_tensors()

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    camera = utils.cv2.VideoCapture(0)


global capture, photo_name

capture = 0
switch = 1
photo_name = None

try:
    os.mkdir('./' + IMG_FOLDER)
except OSError as error:
    pass

def gen_frames():
    global capture, photo_name
    while True:
        success, frame = camera.read() 
        if success:
            if capture:
                capture = 0
                p = os.path.sep.join([IMG_FOLDER, photo_name + ".png"])
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
def predict_tflite():
    time.sleep(3)
    image = utils.read_image(photo_name + ".png")
    accuracy, label_predicted, rest = pred.predict_tflite(image, interpreter)
    return render_template('prediction.html', label=label_predicted, accuracy=accuracy, photo=photo_name + ".png")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/api/take_photo', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type', 'Authorization'])
def take_photo():
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture, photo_name
            new_img_name = request.form.get('photo_name')
            if os.path.exists(os.path.sep.join([IMG_FOLDER, new_img_name])):
                return make_response("Error, there already exists and image with this name.", 400)
                # IMPROVE BAD REQUEST
            else:
                capture = 1
                photo_name = new_img_name
                return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        f = utils.open_labels_csv()
        labels = ""
        if request.form.keys == 1:
            labels = str(request.form.get('approvedLabels'))
        else:
            for label in request.form.values():
                labels += label + " "
            labels = labels[:-1]
        f.write(photo_name + '.png' + ',' + labels + '\n')
        f.close()
    return make_response(labels, 200)

if __name__ == '__main__':
    app.run(debug=True)
