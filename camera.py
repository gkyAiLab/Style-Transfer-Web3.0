import cv2, os
from imutils.video import WebcamVideoStream
import torch
from model.style_transfer import transformer, utils

class VideoCamera(object):
    def __init__(self, style=None):
        # init recording
        self.with_camera = False
        self.style = style  # choose a style or origin webcam stream
        self.init_camera()
        self.recording_init()
        self.init_style_transfer(style)
    
    def init_style_transfer(self, style):
        # Load Transformer Network
        style_transfer_model_path = 'model/style_transfer/transforms'

        device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device

        print("Loading Transformer Network")
        net = transformer.TransformerNetwork()

        if style != None:
            model_name = style + '.pth'
        else:
            model_name = 'mosaic.pth'
        style_transform_path = os.path.join(style_transfer_model_path, model_name)
        net.load_state_dict(torch.load(style_transform_path))
        self.net = net.to(device)
        print("Done Loading Transformer Network")  

    def init_camera(self):
        self.with_camera = True
        # self.stream = WebcamVideoStream(src=0).start()
        self.stream = cv2.VideoCapture(0)

    def close_camera(self):
        self.with_recording = False
        self.recording_index = 0
        self.stream.release()

    def recording_init(self):
        # init recording path
        self.with_recording = False
        self.recording_index = 0
        self.recording_video_path = os.path.join(os.getcwd(), 'video')
        self.recording_video_frames = os.path.join(self.recording_video_path, 'buffer')

        if not os.path.exists(self.recording_video_frames):
            os.mkdir(self.recording_video_frames)

        file_list = os.listdir(self.recording_video_frames)
        for file in file_list:
            frame = os.path.join(self.recording_video_path, file)
            if os.path.exists(frame):
                os.remove(frame)

    def recording_end(self):
        # recording End
        self.with_recording = False
        self.recording_index = 0

    def recording(self, image):
        # recording each image
        frame_name = "{:08d}.png".format(self.recording_index)
        frame_name = os.path.join(self.recording_video_frames, frame_name)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(frame_name, image)
        self.recording_index += 1

    def __del__(self):
        # print(self.style)
        # print('*************************************')
        # self.stream.stop()
        self.stream.release()

    def transfer_image(self, image):
        "transfer function"
        # Free-up unneeded cuda memory
        torch.cuda.empty_cache()      
        # Generate image
        content_tensor = utils.itot(image).to(self.device)
        generated_tensor = self.net(content_tensor)
        generated_image = utils.ttoi(generated_tensor.detach())
        return generated_image
    
    def get_webcam_stream(self):
        """Get a origin image from webcam"""
        _, image = self.stream.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return _, data

    def get_style_transfer_frame(self):
        "Style Transfer Function"
        _, image = self.stream.read()
        generated_image = self.transfer_image(image)

        if self.with_recording:
            self.recording(generated_image)
            
        ret, jpeg = cv2.imencode('.jpg', generated_image)  
        data = []
        data.append(jpeg.tobytes())
        return _, data



        
        