import os
import torch
##########matting###############
from matting import *
from matting.stylematting import * 

class Config():
    def __init__(self, style_init_down='False',with_record='False', record_index = '0', with_webcam='False', style_model = 'None', with_style = 'False',with_matting='False',input_model='0'):
        self.with_webcam = with_webcam  # 是否打开摄像头
        
        self.sytle_model = style_model  # 风格迁移模型的名称
        self.with_style = with_style  # 是否使用风格迁移
        self.change_style_model = 'False'  # 风格迁移模型是否改变 self.style_change

        self.with_matting=with_matting # self.model_mat='1' 抠图
        self.input_model=input_model #self.stat_mat self.input

        self.with_record = with_record  # 是否开始录制
        self.record_index = record_index  # 视频录制的下标

        self.matting_init = 'False' # 抠图功能的背景是否初始化
        self.with_matting = 'False'  # 是否使用抠图功能

        work_dir = os.getcwd()  # 获得当前的工作路径

        self.matting_background = os.path.join(work_dir, 'matting_background')
        
        # 初始化视频帧的保存地址
        video_frames_buffer = os.path.join(work_dir, 'video') # 初始化视频帧的保存地址
        self.video_frames_buffer = os.path.join(video_frames_buffer, 'buffer')

        self.video_complete = False  # 视频是否合成
        self.start_video_complete = False

        self.with_take_pictures = False  # 是否使用拍照
        self.take_picture_complete = False # 排好的照片是否保存完毕

        self.picture_name = None  # 记录照片的文件名
        self.with_print_photo = False  # 是否打印照片

        self.video_out_name = None  # 当前合成的视频名

        #######################################
        #open camera init style ,update self.net
        self.style_init_down=style_init_down
        self.init_style_transfer(self.sytle_model)
        BGModel.reload(self)

        # 初始化拍照功能
        self.init_take_pictures()

        # 初始化二维码路径
        self.init_qrcode_path()

        # 初始化视频保存路径
        self.init_record_path()

    # 初始化视频录制地址
    def init_record_path(self):
        video_path = os.path.join(os.getcwd(),'video')
        if not os.path.exists(video_path):
            os.mkdir(video_path)
        
        video_buffer_path = os.path.join(video_path, 'buffer')
        if not os.path.exists(video_buffer_path):
            os.mkdir(video_buffer_path)

    # 初始化拍照功能路径 
    def init_take_pictures(self):
        picture = os.path.join(os.getcwd(), 'static')
        picture = os.path.join(picture, 'picture')
        if not os.path.exists(picture):
            os.mkdir(picture)
            self.picture_path = picture

    # 初始化二维码路径
    def init_qrcode_path(self):
        qrcode_path = os.path.join(os.getcwd(), 'static')
        qrcode_path = os.path.join(qrcode_path, 'qrcode')

        if not os.path.exists(qrcode_path):
            os.mkdir(qrcode_path)

    def init_style_transfer(self, style):
        # Load Transformer Network
        style_transfer_model_path = 'model/style_transfer/transforms'

        device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device

        print("Loading Transformer Network")
        net = transformer.TransformerNetwork()

        if style != 'None':
            print("style != None")
            model_name = style + '.pth'
        else:
            model_name = 'mosaic.pth'
        style_transform_path = os.path.join(style_transfer_model_path, model_name)
        net.load_state_dict(torch.load(style_transform_path))
        self.net = net.to(device)
        print("Done Loading Transformer Network") 

    def refresh(self):
        # 刷新状态
        self.with_webcam = 'False'
        self.with_style = 'False'
        self.with_matting='False'

        self.with_record = 'False'
        self.record_index = '0'

        self.matting_init = 'False'
        self.with_matting = 'False'  

        self.video_complete = 'False'

        self.input_model='0' 
    def refresh_init_style(self):
        # 刷新状态
        self.with_style = 'False'
        self.with_matting='False'

        self.with_record = 'False'
        self.record_index = '0'

        self.matting_init = 'False'
        self.with_matting = 'False'  

        self.video_complete = 'False'

        self.input_model='0'
        self.sytle_model='None'
        self.change_style_model = 'True'

    
    # 删除所有的视频帧
    def clear_video_frames(self):
        file_list = os.listdir(self.video_frames_buffer)
        for file in file_list:
            frame = os.path.join(self.video_frames_buffer, file)
            if os.path.exists(frame):
                print("{} has been removed.".format(frame))
                os.remove(frame)

        print('All Frames have been removed !!')
    
    # 删除抠图的初始化图像
    def clear_matting_image(self):
        matting_image_name = os.path.join(self.matting_background, "matting_backgroud.png")
        if os.path.exists(matting_image_name):
            os.remove(matting_image_name)
            print("{} has been removed.".format(matting_image_name))
    
     # 删除二维码
    def clear_qrcode(self):
        qrcode_path = os.path.join(os.getcwd(), 'static')
        qrcode_path = os.path.join(qrcode_path, 'qrcode')

        if os.path.exists(qrcode_path):
            file_list = os.listdir(qrcode_path)

            for file in file_list:
                frame = os.path.join(qrcode_path, file)
                if os.path.exists(frame):
                    print("{} has been removed.".format(frame))
                    os.remove(frame)

    # 删除所有保存的视频
    def clear_videos(self):
        video_path = os.path.join(os.getcwd(), 'video')

        if os.path.exists(video_path):
            video_list = os.listdir(video_path)
            for video in video_list:
                video_name = os.path.join(video_path, video)

                if os.path.isfile(video_name):
                    file_end = video.split('.')[1]
                    if file_end == 'mp4':
                        os.remove(video_name)
                        print("{} has been removed.".format(video_name))

