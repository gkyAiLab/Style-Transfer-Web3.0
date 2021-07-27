import cv2
import base64

def get_image(camera):
    """Get Face recognition image"""
    while True:
        data= camera.get_frame()
        frame = data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_style_transfer_image(camera):
    """Get style transfer image"""
    while True:
        data = camera.get_style_transfer_frame()
        frame = data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_webcam_image(camera):
    """Get origin image from webcam"""
    while True:
        data = camera.get_webcam_stream()
        frame = data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

