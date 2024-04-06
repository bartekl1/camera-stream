from flask import Flask, render_template, send_file, Response
import cv2

import threading
import datetime
import time
import json

with open("configs.json") as file:
    configs = json.load(file)

app = Flask(__name__)

camera_frame = None


def generate_frames():
    global camera_frame
    vs = cv2.VideoCapture(0)
    while True:
        ret, frame = vs.read()

        if "rotate" in configs.keys():
            if configs["rotate"] == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif configs["rotate"] == 180:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif configs["rotate"] == 270:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        flip_vertically = "flip_vertically" in configs.keys() and configs["flip_vertically"]
        flip_horizontally = "flip_horizontally" in configs.keys() and configs["flip_horizontally"]
        if flip_vertically and flip_horizontally:
            frame = cv2.flip(frame, -1)
        elif flip_vertically and not flip_horizontally:
            frame = cv2.flip(frame, 0)
        elif flip_horizontally and not flip_vertically:
            frame = cv2.flip(frame, 1)

        dt = datetime.datetime.now()
        dt_text = dt.strftime("%Y.%m.%d %H:%M:%S")
        frame = cv2.putText(img=frame,
                            text=dt_text,
                            org=(5, 20),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6,
                            color=(255, 255, 255),
                            thickness=1,
                            lineType=cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        camera_frame = (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(0.1)


def get_frame():
    while camera_frame is None:
        time.sleep(0.1)
    while True:
        yield camera_frame
        time.sleep(0.1)


@app.before_first_request
def start_thread():
    generator_thread = threading.Thread(target=generate_frames)
    generator_thread.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/favicon.ico')
def favicon():
    return send_file('static/img/favicon.ico')


if __name__ == '__main__':
    host = configs["host"] if "host" in configs.keys() else None
    port = configs["port"] if "port" in configs.keys() else None
    debug = configs["debug"] if "debug" in configs.keys() else None
    app.run(host=host, port=port, debug=debug)
