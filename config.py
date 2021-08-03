class Config():
    def __init__(self, with_record=False, record_index = 0, with_webcam=False, style_model = None, with_style = False):
        self.with_webcam = with_webcam  # 是否打开摄像头
        
        self.sytle_model = style_model  # 风格迁移模型的名称
        self.with_style = with_style  # 是否使用风格迁移
        self.change_style_model = False  # 风格迁移模型是否改变

        self.with_record = with_record  # 是否开始录制
        self.record_index = 0  # 视频录制的下标

