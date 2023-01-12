from flask import Flask, render_template, Response
from camera import VideoCamera
import time
import os

app = Flask(__name__)
picFolder = os.path.join('static', 'pics')
prev = 0

app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'wave-bottom.svg')
    return render_template('index.html', user_image=pic1)

def gen(camera):
    while True:
        time_elapsed = time.time() - prev
        try:
            frame = camera.get_frame(time_elapsed)
            yield (b'--frame\r\n'
                b'Content-Type:image/jpeg\r\n\r\n' + frame 
                + b'\r\n\r\n')
        except:
            frame = camera.get_frame_original()
            yield (b'--frame\r\n'
                b'Content-Type:image/jpeg\r\n\r\n' + frame 
                + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__== '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)