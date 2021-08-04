from genericpath import exists
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import cv2, os
from config import Config
from GenerateQrcode import Gnerate_qrcode

app = Flask(__name__)
state = Config() 

def gen(camera):
    # 这个是主要功能，返回给路由视频帧
    while True:
        # 检测当前是否打开了摄像头
        if state.with_webcam == False:
            break

        # 从摄像头获取每一帧
        success, frame = camera.get_frame()

        if state.matting_init:
            matting_frame_name = os.path.join(state.matting_background, 'matting_backgroud.png')
            cv2.imwrite(matting_frame_name, frame)
            state.matting_init = False # 初始化后就把初始化信号更新

        # 是否使用风格迁移
        if state.with_style == False:
            success, data = camera.img_to_bytes(success, frame)
        else:
            # 检测模型是否改变，改变了的话就重新加载一下预训练模型
            if state.change_style_model == True:
                camera.init_style_transfer(state.sytle_model)
                state.change_style_model = False

            frame = camera.transfer_image(frame)
            success, data = camera.img_to_bytes(success, frame)
        
        if state.with_record == True:
            image_name_index = "{:08d}.png".format(camera.recording_index)
            image_name = os.path.join(camera.recording_video_frames, image_name_index)
            print('image_name：', image_name)
            cv2.imwrite(image_name, frame)
            camera.recording_index += 1
        else:
            camera.recording_end()  # 结束录制
            
            if state.video_complete != True: # 如果视频还没有合成好，就合成一次
                Gnerate_qrcode(state.video_frames_buffer) # 合成视频、生成二维码、改变状态变量
                state.video_complete = True # 告诉前端，视频已经合成好了

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
    print('Enter style transfer page!!')
    state.refresh() # 更新状态变量
    state.clear_video_frames() # 删除之前保存的视频帧
    state.clear_matting_image() # 删除所有抠图初始化的图像
    state.clear_qrcode()  # 删除二维码

    return render_template('style_transfer.html')

@app.route('/webcam_stream')
def webcam_stream():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/get_qrcode')
# def get_qrcode():
#     qrcode_image = cv2.imread('./static/qrcode/qrcode_out.png')
#     ret, jpeg = cv2.imencode('.jpg', qrcode_image)
#     frame = jpeg.tobytes()


@app.route('/update', methods=['POST'])
def update():  
    # 修改配置文件功能：录制，转换风格
    if request.method == 'POST':
        # 接收录制的信号
        try:
            with_record = request.form['with_record']
            if with_record == 'True':
                state.with_record = True
            else:
                state.with_record = False
                state.video_complete = False

            print('with_record: ', with_record)
            print('video complete: ', state.video_complete)
            return jsonify({'with_record' : with_record})
        except:
            with_record = state.with_record

        # 接收是否打开摄像头的信号
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
        
        # 接收改变风格的信号
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
            # print('Load style transfer button: False !!')
            with_style = state.with_style
        
        # 接收抠图的信号
        try:
            matting_init = request.form['matting_init']
            state.matting_init = matting_init
            print('state with_matting_init: ', state.matting_init)
            return jsonify({'matting_init' : matting_init})
        except:
            matting_init = state.matting_init
        
        # 接收视频二维码上传信号
        try:
            video_complete = request.form['video_complete']
            state.video_complete = video_complete
            print('video complete: ', state.video_complete)
            return jsonify({'video_complete' : video_complete})
        except:
            video_complete = state.video_complete


# 后端的状态反馈给前端
@app.route('/update_flask_state')
def update_flask_state():
    state_dict = {
        'with_webcam' : state.with_webcam,
        'with_style' : state.with_style,
        'video_complete' : state.video_complete
    }
    return jsonify(state_dict)

@app.route('/TODO')
def TODO():
    return "TODO"

if __name__=="__main__":
    app.run(debug=True)



