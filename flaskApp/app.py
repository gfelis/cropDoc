from flask import Flask, render_template, Response, request
from flask.helpers import make_response
from flask_cors import CORS, cross_origin

import model.utils as utils
import model.predictions as pred

import parser.ConfigurationFile as conf
import parser.GenerateKml as gkml
import parser.global_vars as gvars
import parser.kml_utils as kml_utils
import parser.parser as Parser

import os, time
import cv2

MODEL_TFLITE = "model.tflite"
IMG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/shots')

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})

interpreter = utils.load_tflite_interpreter(MODEL_TFLITE)
interpreter.allocate_tensors()

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), utils.cv2.CAP_GSTREAMER)


global capture, photo_name

capture = 0
switch = 1
photo_name = None

try:
    os.mkdir(IMG_FOLDER)
    os.chmod(IMG_FOLDER, mode=0o777)
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
                print("Taking photo...")
                print("\tSaving on: " + p)
                print("\tResolution: " + str(frame.shape))
                if os.path.isdir(IMG_FOLDER):
                    retval = cv2.imwrite(p, frame)
                    print("\tSaving has been succesful!") if retval else print("\tError, couldn't save image.")
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
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
            else:
                capture = 1
                photo_name = new_img_name
                return make_response("Taking photo...")


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

@app.route('/api/demo', methods=['POST'])
def demo():
    if request.method == 'POST':
        if request.form.get('do') == 'play':
            conf.LoadConfigFile()
            p = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), 'static/xls/jorge_gil.xlsx'])
            print(p)
            if os.path.exists(p):
                fields = Parser.parse(p)
            for field in fields:
                gkml.CreateKML(fields[field])
                kml_utils.sendKmlToLG(gvars.kml_destination_filename)
                kml_utils.flyToField(fields[field], 360)
                time.sleep(18.2)
    return make_response(200)

@app.route('/api/clean', methods=['POST'])
def clean():
    kml_utils.cleanKMLFiles()
    return make_response(200)

if __name__ == '__main__':   
    app.run(debug=True)
