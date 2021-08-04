import os

class Config():
    def __init__(self, with_record=False, record_index = 0, with_webcam=False, style_model = 'origin', with_style = False):
        self.with_webcam = with_webcam  # 是否打开摄像头
        
        self.sytle_model = style_model  # 风格迁移模型的名称
        self.with_style = with_style  # 是否使用风格迁移
        self.change_style_model = False  # 风格迁移模型是否改变

        self.with_record = with_record  # 是否开始录制
        self.record_index = record_index  # 视频录制的下标

        self.matting_init = False # 抠图功能的背景是否初始化
        self.with_matting = False  # 是否使用抠图功能

        work_dir = os.getcwd()  # 获得当前的工作路径

        self.matting_background = os.path.join(work_dir, 'matting_background')
        
        # 初始化视频帧的保存地址
        video_frames_buffer = os.path.join(work_dir, 'video')
        self.video_frames_buffer = os.path.join(video_frames_buffer, 'buffer')

    def refresh(self):
        # 刷新状态
        self.with_webcam = False
        self.with_style = False

        self.with_record = False
        self.record_index = 0

        self.matting_init = False
        self.with_matting = False  
    
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


