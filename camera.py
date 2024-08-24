import sys
import cv2

class Camera:
    def __init__(self, camera_id):
        self.camera_id = camera_id

        self.camera = None
        self.camera_writer = None

        self.is_streaming = False
        self.is_recording = False

    def read_frame(self):
        frame = self.camera.read()

        return frame

    def toggle_streaming(self):
        if self.is_streaming:
            self.stop_streaming()
        else:
            self.start_streaming()

    def start_streaming(self):
        self.camera = cv2.VideoCapture(self.camera_id)
        self.is_streaming = True

    def stop_streaming(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.is_streaming = False

    def toggle_recording(self):
        pass

    def start_recording(self):
        pass

    def stop_recording(self):
        pass
