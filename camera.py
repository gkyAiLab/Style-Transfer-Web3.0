import cv2
import pickle
from imutils.video import WebcamVideoStream
import face_recognition
import torch
from model.style_transfer import transformer, utils


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        # Device
        device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device

        # Load Transformer Network
        print("Loading Transformer Network")
        net = transformer.TransformerNetwork()

        style_transform_path = 'mosaic.pth'
        
        net.load_state_dict(torch.load(style_transform_path))
        net = net.to(device)
        self.net = net
        print("Done Loading Transformer Network")

        # Read video stream
        self.stream = WebcamVideoStream(src=0).start()
        with open("trained_knn_model.clf", 'rb') as f:
            self.knn_clf = pickle.load(f)

    def __del__(self):
        self.stream.stop()

    def predict(self, frame, knn_clf, distance_threshold=0.4):
        # Find face locations
        X_face_locations = face_recognition.face_locations(frame)

        if len(X_face_locations) == 0:
            return []

        # Find encodings for faces in the test iamge
        faces_encodings = face_recognition.face_encodings(frame, known_face_locations=X_face_locations)

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
        for i in range(len(X_face_locations)):
            print("closest_distances")
            print(closest_distances[0][i][0])

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
                zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    def get_frame(self):
        # Face Recognition
        image = self.stream.read()
        li = []
        global person_name
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        f = open("trainStatus.txt")
        for i in f:
            isTrained = int(i)
        if isTrained:  # change updated model file
            # load again
            with open("trained_knn_model.clf", 'rb') as f:
                self.knn_clf = pickle.load(f)
            file = open("trainStatus.txt", "w")
            file.write("0")
            file.close()
        predictions = self.predict(image, self.knn_clf)
        name = ''
        for name, (top, right, bottom, left) in predictions:
            startX = int(left)
            startY = int(top)
            endX = int(right)
            endY = int(bottom)

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(image, name, (endX - 70, endY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        data.append(name)
        return data
    
    def get_webcam_stream(self):
        """Get a origin image from webcam"""
        image = self.stream.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data

    
    def transfer_image(self, image):
        "transfer function"
        # Free-up unneeded cuda memory
        torch.cuda.empty_cache()      
        # Generate image
        content_tensor = utils.itot(image).to(self.device)
        generated_tensor = self.net(content_tensor)
        generated_image = utils.ttoi(generated_tensor.detach())
        return generated_image

    def get_style_transfer_frame(self):
        "Style Transfer Function"
        image = self.stream.read()
        cv2.imwrite("./static/buffer/web_stream.png", image)  # Save a temprory image for origin stream
        generated_image = self.transfer_image(image)
        ret, jpeg = cv2.imencode('.jpg', generated_image)
        data = []
        data.append(jpeg.tobytes())
        return data



        
        