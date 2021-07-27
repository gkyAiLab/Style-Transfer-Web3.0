import json,time
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response,  redirect, url_for
import requests
import base64,cv2
from utils import get_image, get_style_transfer_image, get_webcam_image

app = Flask(__name__)
output=[] # ("message stark","hi")]

@app.route('/')
def home_page():
    return render_template("home.html",result=output)

@app.route('/webcam_stream')
def webcam_stream():
    return Response(get_webcam_image(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/face_recognition')
def face_recognition():
    return Response(get_image(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/style_transfer')
def style_transfer():
    return render_template('style_transfer.html')

@app.route('/style_transfer_stream')
def style_transfer_stream():
    return Response(get_style_transfer_image(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return render_template('test.html')

if __name__=="__main__":
    app.run(debug=True)



