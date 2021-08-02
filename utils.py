def get_webcam_image(camera):
    """Get origin image from webcam"""
    # camera.init_camera()
    while True:
        success, data = camera.get_webcam_stream()
        if success:
            frame = data[0]
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break

def get_style_transfer_image(camera):
    """Get style transfer image"""
    # camera.init_camera()
    while True:
        success, data = camera.get_style_transfer_frame()
        if success:
            frame = data[0]
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break


