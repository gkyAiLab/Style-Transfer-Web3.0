import json, time
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response,  redirect, url_for
import requests
import base64, cv2
from utils import get_webcam_image, get_style_transfer_image

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/style_transfer')
def style_transfer():
    return render_template('style_transfer.html')

@app.route('/webcam_stream')
def webcam_stream():
    return Response(get_webcam_image(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_mosaic')
def webcam_stream_mosaic():
    style = 'mosaic'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_bayanihan')
def webcam_stream_bayanihan():
    style = 'bayanihan'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_lazy')
def webcam_stream_lazy():
    style = 'lazy'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_starry')
def webcam_stream_starry():
    style = 'starry'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_tokyo_ghoul')
def webcam_stream_tokyo_ghoul():
    style = 'tokyo_ghoul'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_udnie')
def webcam_stream_udnie():
    style = 'udnie'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_wave')
def webcam_stream_wave():
    style = 'wave'
    return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)



