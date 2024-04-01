from flask import Flask, render_template, Response
import cv2

import threading
import datetime
import time

app = Flask(__name__)

camera_frame = None


def generate_frames():
    global camera_frame
    vs = cv2.VideoCapture(0)
    while True:
        ret, frame = vs.read()
        dt = datetime.datetime.now()
        dt_text = dt.strftime("%Y.%m.%d %H:%M:%S")
        frame = cv2.putText(img=frame,
                            text=dt_text,
                            org=(5, 20),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5,
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
