from genericpath import exists
from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import cv2, os
from config import Config

##########matting###############
from matting import *
from matting.stylematting import * 


app = Flask(__name__)
state = Config() 
##########recording and photo ################
from GenerateQrcode import Gnerate_video_qrcode, Gnerate_picture_qrcode
from print_photo_web import MainWindow
from PyQt5.QtWidgets import QApplication
##########end ################


def _get_image(state,image):
        img = matting_model.transfer_image_style(state,image)  # tranfer style
        # img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB).clip(0,255)
        img=img.clip(0,255)
        norm_img=img.astype(np.uint8)
        return norm_img
def mat_style(input,style_type,camera):
        print("matting")
        flag, state.image = camera.get_frame()  # 从视频流中读取 
        state.image = matting_model.matting_step(state,state.image,input,style_type)  #matting

        return state.image

def gen(camera):
    # 这个是主要功能，返回给路由视频帧
    while True:
        # 检测当前是否打开了摄像头
        if state.with_webcam == 'False':
            break

        # 从摄像头获取每一帧
        success, frame = camera.get_frame()
        state.image=frame
        # print(state.matting_init,"state.matting_init&&&&")

        if state.matting_init=='True':#choose background
            # #save img
            # matting_frame_name = os.path.join(state.matting_background, 'matting_backgroud.png') #choose bg as img
            # cv2.imwrite(matting_frame_name, frame)
            # # app
            VideoCamera.matting(state,state.image)
            state.matting_init = 'False' # 初始化后就把初始化信号更新
        # print("&&&&&&&&&&&&&&&&&&&&&&&&",state.style_init_down)
        if state.style_init_down=='True':
            state.refresh_init_style()
            state.style_init_down='False'
        
        if state.with_matting=='True':
            # print('%%%%%%%%%%%%%%%%%%with_matting',state.with_matting)
            print(state.input_model)
            print(state.sytle_model)
            if state.input_model=='1':
                state.image =mat_style(input=state.input_model,style_type=state.sytle_model,camera=camera)

                success, data = camera.img_to_bytes(success, state.image)
            if state.input_model=='2':
                state.image =mat_style(input=state.input_model,style_type= state.sytle_model,camera=camera)
                success, data = camera.img_to_bytes(success, state.image)
            if state.input_model=='3':
                state.image =mat_style(input=state.input_model,style_type= state.sytle_model,camera=camera)
                success, data = camera.img_to_bytes(success, state.image)
        else:
            # print("&&&&&&&&&&&&&&&&&&&&&&&&no matting  style or open camera",state.with_style)
            ##################################################################################################
            # 是否使用风格迁移
            if state.with_style == 'False':
                success, data = camera.img_to_bytes(success, state.image)
            else:
                # 检测模型是否改变，改变了的话就重新加载一下预训练模型
                if state.change_style_model == 'True':
                    matting_model.preload_init(state)

                    # camera.init_style_transfer(state.sytle_model)
                    state.change_style_model = 'False'

                # frame = camera.transfer_image(frame)
                state.image=_get_image(state,state.image)
                success, data = camera.img_to_bytes(success, state.image)
            ##################################################################################################
        frame=state.image
        # 是否进行录制
        if state.with_record == 'True':
            image_name_index = "{:08d}.png".format(camera.recording_index)
            image_name = os.path.join(camera.recording_video_frames, image_name_index)
            print('image_name：', image_name)
            cv2.imwrite(image_name, frame)
            camera.recording_index += 1
        else:
            camera.recording_end()  # 结束录制
            
            if state.start_video_complete == 'True': # 如果视频还没有合成好，就合成一次
                state.start_video_complete = 'False' 

                if state.with_style=='True':
                    video_out_name, video_qrcode = Gnerate_video_qrcode(state.video_frames_buffer, fps=8, with_transfer=True) # 合成视频、生成二维码、改变状态变量
                else: 
                    video_out_name, video_qrcode = Gnerate_video_qrcode(state.video_frames_buffer)

                if video_qrcode != 'False':
                    state.video_complete = 'True' # 告诉前端，视频已经合成上传好了
                    print("Video Complete !")
                    
        # 是否进行拍照
        if state.with_take_pictures=='True':
            # c = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
            c = 'picture'
            picture_name = '{}.png'.format(c)
            picture_path = os.path.join(os.getcwd(), 'static')
            picture_path = os.path.join(picture_path, 'picture')
            photo_name = os.path.join(picture_path, picture_name)
            cv2.imwrite(photo_name, frame)

            Gnerate_picture_qrcode(picture_path) # 上传图片
            
            state.with_take_pictures = 'False'
            state.picture_name = picture_name  # 记录照片的文件名
            state.take_picture_complete = 'True' # 告诉照片已经保存好了
        
        if state.with_print_photo == 'True':
            app = QApplication(sys.argv)
            main = MainWindow()
            main.slotPrint()

            print("Print Finished !")
            state.with_print_photo = 'False'
            
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



@app.route('/update', methods=['POST'])
def update():  
    # 修改配置文件功能：录制，转换风格
    if request.method == 'POST':
        # 接收save img 的信号
        try:
            matting_init = request.form['matting_init']
            state.matting_init = matting_init
            print('!!!state with_matting_init: ', state.matting_init)
            return jsonify({'matting_init' : matting_init})
        except:
            matting_init = state.matting_init
        # 接收录制的信号
        try:
            with_record = request.form['with_record']
            start_video_complete = request.form['start_video_complete']
            video_complete = request.form['video_complete']
            print('video_complete: ', video_complete)

            if with_record == 'True':
                state.with_record = 'True'
            else:
                state.with_record = 'False'
                
            if start_video_complete == 'True':    
                state.start_video_complete = 'True'
            else: state.start_video_complete = 'False'

            if video_complete == 'False':
                state.video_complete = 'False'

            print('with_record: ', with_record)
            print('start_video_complete: ', state.start_video_complete)
            print("video_complete: ", state.video_complete)
            return jsonify({'with_record' : with_record})
        except:
            with_record = state.with_record

         # 拍照功能
        try:
            with_take_pictures = request.form['with_take_pictures']
            print('是否拍照: ', with_take_pictures)
            if with_take_pictures == 'True':
                state.with_take_pictures = 'True'
            
            return jsonify({'with_take_pictures': with_take_pictures})
        except:
            with_take_pictures = state.with_take_pictures
        
        try:
            print_photo = request.form['print_photo']
            state.with_print_photo = 'True'
            print('打印信号: ', print_photo)
            return jsonify({'print_photo' : print_photo})
        except:
            print_photo = 'asdjgil'

        # 接收是否打开摄像头的信号
        try:
            with_webcam = request.form['with_webcam']
            if with_webcam == 'True':
                state.with_webcam = 'True'
            else:
                state.with_webcam = 'False'

            print('with_webcam: ', with_webcam)
            return jsonify({'with_webcam' : with_webcam})
        except:
            with_webcam = state.with_webcam
        
        # 接收init_cam的信号 add
        try:
            style_init_down=request.form['style_init_down']
            state.style_init_down=style_init_down


            # with_style = request.form['with_style']
            # with_matting = request.form['with_matting']
            # change_model = request.form['change_model']
            # input_model = request.form['input_model']
            # sytle_model=request.form['sytle_model']

            # state.with_matting = with_matting
            # state.input_model=input_model
            # state.sytle_model=sytle_model
            # print('with_style: ', with_style)
            # print('state with_matting: ', state.with_matting)
            # print('input_model no matting',state.input_model)

            state.change_style_model = 'True'
            # # 模型是否更换
            # if change_model == 'True':  
            #     state.change_style_model = 'True'
            # else:
            #     state.change_style_model = 'False'
            
            # # 是否使用了风格迁移 
            state.with_style = 'False'

            return jsonify({'change_style_model' : state.change_style_model})
        except:
            with_matting = state.with_matting


        # 接收no matting的信号 add
        try:
            # sytle_model=request.form['sytle_model']
            with_style = request.form['with_style']
            with_matting = request.form['with_matting']
            change_model = request.form['change_model']
            input_model = request.form['input_model']
            
            state.with_matting = with_matting
            state.input_model=input_model
            # state.sytle_model=sytle_model
            
            print('with_style: ', with_style)
            print('state with_matting: ', state.with_matting)
            print('input_model no matting',state.input_model)

            # 模型是否更换
            if change_model == 'True':  
                state.change_style_model = 'True'
            else:
                state.change_style_model = 'False'
            
            # 是否使用了风格迁移 
            if with_style == 'True':
                state.with_style = 'True'
            else:
                state.with_style = 'False'

            return jsonify({'with_matting' : with_matting})
        except:
            with_matting = state.with_matting


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
                state.change_style_model = 'True'
            else:
                state.change_style_model = 'False'

            # 是否使用了风格迁移 
            if with_style == 'True':
                state.with_style = 'True'
            else:
                state.with_style = 'False'
            return jsonify({'with_style' : with_style})
        except:
            # print('Load style transfer button: False !!')
            with_style = state.with_style
        
        

        # 接收matting的信号 add
        try:
            with_matting = request.form['with_matting']
            change_model = request.form['change_model']
            input_model = request.form['input_model']

            state.with_matting = with_matting
            state.input_model=input_model
            print('state with_matting: ', state.with_matting)
            print('input_model',state.input_model)

            # 模型是否更换
            if change_model == 'True':  
                state.change_style_model = 'True'
            else:
                state.change_style_model = 'False'

            return jsonify({'with_matting' : with_matting})
        except:
            with_matting = state.with_matting
        
        


        # 接收视频二维码上传信号
        try:
            video_complete = request.form['video_complete']
            state.video_complete = video_complete
            print('video complete: ', state.video_complete)
            return jsonify({'video_complete' : video_complete})
        except:
            video_complete = state.video_complete
            #change
            return jsonify({'None'})




# 后端的状态反馈给前端
@app.route('/update_flask_state')
def update_flask_state():
    state_dict = {
        'with_webcam' : state.with_webcam,
        'with_style' : state.with_style,
        'video_complete' : state.video_complete,
        'take_picture_complete': state.take_picture_complete
    }

    # 一部分信号给前端传输后，直接改回默认值就可以了
    if state.take_picture_complete == 'True':
        state.take_picture_complete = 'False' 
    


    print(state_dict)
    return jsonify(state_dict)

if __name__=="__main__":
    app.run(debug=True)



