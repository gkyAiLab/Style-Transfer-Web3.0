import json, time
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response,  redirect, url_for
import requests
import base64, cv2, os
from utils import get_webcam_image, get_style_transfer_image
from config import Config

app = Flask(__name__)
state = Config() 

def gen(camera):
    while True:
        if state.with_webcam == False:
            break

        success, frame = camera.get_frame()
        if state.with_style == False:
            success, data = camera.img_to_bytes(success, frame)
        else:
            frame = camera.transfer_image(frame)
            success, data = camera.img_to_bytes(success, frame)
        
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
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_stream_mosaic')
def webcam_stream_mosaic():
    state.with_style = True
    style = 'mosaic'
    if state.with_webcam:
        return Response(gen(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Please Open Webcam !"

@app.route('/webcam_stream_bayanihan')
def webcam_stream_bayanihan():
    style = 'bayanihan'
    if state.with_webcam:
        return Response(get_style_transfer_image(VideoCamera(style)), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Please Open Webcam !"

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
        try:
            with_record = request.form['with_record']
            if with_record == 'True':
                state.with_record = True
            else:
                state.with_record = False

            print('with_record: ', with_record)
            return jsonify({'with_record' : with_record})
        except:
            with_record = state.with_record

        try:
            with_webcam = request.form['with_webcam']
            if with_webcam == 'True':
                state.with_webcam = True
            else:
                state.with_webcam = False

            print('with_webcam: ', with_webcam)
            return jsonify({'with_webcam' : with_webcam})
        except:
            with_webcam = state.with_webcam
        
        try:
            with_style = request.form['with_style']
            style_model = request.form['transfer_style']
            change_model = request.form['change_model']

            state.sytle_model = style_model

            print('with_style: ', with_style)
            print('style_model: ', style_model)
            print('if changed: ', change_model)
            
            # 模型是否更换
            if change_model == 'True':  
                state.change_style_model = True
            else:
                state.change_style_model = False

            # 是否使用了风格迁移 
            if with_style == 'True':
                state.with_style = True
            else:
                state.with_style = False
            return jsonify({'with_style' : with_style})
        except:
            with_style = state.with_style
        
@app.route('/update_flask_state')
def update_flask_state():
    # 后端的状态反馈给前端
    state_dict = {
        'with_webcam' : state.with_webcam,
        'with_style' : state.with_style,
    }
    return jsonify(state_dict)

@app.route('/TODO')
def TODO():
    return "TODO"

if __name__=="__main__":
    app.run(debug=True)



