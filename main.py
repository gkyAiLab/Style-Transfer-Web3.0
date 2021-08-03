import json, time
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response,  redirect, url_for
import requests
import base64, cv2, os
from utils import get_webcam_image, get_style_transfer_image
from config import Config

app = Flask(__name__)
state = Config()   # init config class

def gen(camera):
    while True:
        success, frame = camera.get_frame()

        if state.with_style == False:
            # success, data = camera.get_webcam_stream()
            success, data = camera.img_to_bytes(success, frame)
        else:
            frame = camera.transfer_image(frame)
            success, data = camera.img_to_bytes(success, frame)
            # success, data = camera.get_style_transfer_frame()
        
        if state.with_record == True:
            image_name_index = "{:08d}.png".format(camera.recording_index)
            image_name = os.path.join(camera.recording_video_frames, image_name_index)
            print('image_name： ', image_name)
            cv2.imwrite(image_name, frame)
            camera.recording_index += 1
        else:
            camera.recording_end()  # 结束录制
            # 合成视频、生成二维码 TODO
            # 清除缓冲区 TODO
        if success:
            frame = data[0]
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/style_transfer')
def style_transfer():
    return render_template('style_transfer.html')

@app.route('/webcam_stream')
def webcam_stream():
    state.with_style = False
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/TODO')
def TODO():
    return "TODO"

@app.route('/webcam_stream_mosaic')
def webcam_stream_mosaic():
    state.with_style = True
    style = 'mosaic'
    return Response(gen(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')

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

@app.route('/update', methods=['POST'])
def update():  
    # 修改配置文件功能：录制，转换风格
    if request.method == 'POST':
        with_record = request.form['with_record']
        
        if with_record == 'True':
            state.with_record = True
        else:
            state.with_record = False
    
        return jsonify({'with_record' : with_record})

if __name__=="__main__":
    app.run(debug=True)



