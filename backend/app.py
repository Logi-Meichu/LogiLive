#!/usr/bin/env python
from flask import Flask, render_template, Response
from flask import request, jsonify
from conn import ConnClient
from common import setup_logger
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'HEAD', 'POST', 'OPTIONS'])

class Camera1:

    def __init__(self):
        logger = setup_logger()
        self.camera = ConnClient(host='172.20.10.7', port=9302, logger=logger)
        self.frame = None

        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
    
    def update(self):
        while True:
            frame = self.camera.read()
            self.frame = frame
    
    def get_frame(self):
        while True:
            if self.frame is not None:
                break
        return self.frame
        
class Camera2:

    def __init__(self):
        logger = setup_logger()
        self.camera = ConnClient(host='172.20.10.7', port=9300, logger=logger)
        self.frame = None

        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
    
    def update(self):
        while True:
            frame = self.camera.read()
            self.frame = frame
    
    def get_frame(self):
        while True:
            if self.frame is not None:
                break
        return self.frame


@app.route('/control', methods=['GET', 'POST'])
def api_control():
    logger = setup_logger()
    conn = ConnClient(host='172.20.10.7', port=8300, logger=logger)

    data = request.get_json()
    print(data)
    
    # Blocking call
    result = conn.transmit(data)
    print('result!')
    print(result)
    conn.close()
    return jsonify({
        'status': 'success'
    }), 200

@app.route('/')
def index():
    # region_str = request.args.get('region', '')
    return jsonify({
        'status': 'success'
    }), 200


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen(Camera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen(Camera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    
    app.run(host='172.20.10.7', port=5000, debug=True)