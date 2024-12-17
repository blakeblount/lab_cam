import sys
import cv2
import time
from PyQt6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

class DualCameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LabCam")
        self.init_ui()
        
        # Auto-detect camera indices
        self.cap1, self.cap2 = self.find_cameras()

        # Recording state and variables
        self.recording = False
        self.writer1 = None
        self.writer2 = None
        self.filename = "output"

        # Timers for refreshing the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

    def find_cameras(self):
        cameras = []
        for i in range(5):  # Test indices 0-4
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(cap)
            else:
                cap.release()
        
        if len(cameras) >= 2:
            return cameras[0], cameras[1]
        elif len(cameras) == 1:
            return cameras[0], None
        else:
            return None, None

    def init_ui(self):
        # Layout for video feeds
        self.video_label1 = QLabel("No Feed")
        self.video_label2 = QLabel("No Feed")
        self.video_label1.setFixedSize(640, 480)
        self.video_label2.setFixedSize(640, 480)
        self.video_label1.setStyleSheet("background-color: black; color: white; text-align: center;")
        self.video_label2.setStyleSheet("background-color: black; color: white; text-align: center;")
        
        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_label1)
        video_layout.addWidget(self.video_label2)

        # Controls
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter filename")
        
        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.filename_input)
        control_layout.addWidget(self.record_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(video_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

    def update_frames(self):
        # Read frames from both cameras
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if self.cap1 and self.cap1.isOpened():
            ret1, frame1 = self.cap1.read()
            if ret1:
                cv2.putText(frame1, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                self.display_frame(self.video_label1, frame1)
                if self.recording and self.writer1:
                    self.writer1.write(frame1)
            else:
                self.display_no_feed(self.video_label1)
        else:
            self.display_no_feed(self.video_label1)
        
        if self.cap2 and self.cap2.isOpened():
            ret2, frame2 = self.cap2.read()
            if ret2:
                cv2.putText(frame2, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                self.display_frame(self.video_label2, frame2)
                if self.recording and self.writer2:
                    self.writer2.write(frame2)
            else:
                self.display_no_feed(self.video_label2)
        else:
            self.display_no_feed(self.video_label2)

    def display_frame(self, label, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(q_image))

    def display_no_feed(self, label):
        label.setText("No Feed")

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        # Get filename
        filename = self.filename_input.text().strip()
        if not filename:
            filename = "output"
        self.filename = filename

        # Define codecs and create VideoWriters
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if self.cap1:
            self.writer1 = cv2.VideoWriter(f"{self.filename}_1.avi", fourcc, 20.0, (640, 480))
        if self.cap2:
            self.writer2 = cv2.VideoWriter(f"{self.filename}_2.avi", fourcc, 20.0, (640, 480))

        self.record_button.setText("Stop Recording")
        self.recording = True

    def stop_recording(self):
        self.recording = False
        self.record_button.setText("Start Recording")
        
        if self.writer1:
            self.writer1.release()
        if self.writer2:
            self.writer2.release()
        self.writer1 = None
        self.writer2 = None

    def closeEvent(self, event):
        # Release resources on close
        if self.cap1 and self.cap1.isOpened():
            self.cap1.release()
        if self.cap2 and self.cap2.isOpened():
            self.cap2.release()
        if self.writer1:
            self.writer1.release()
        if self.writer2:
            self.writer2.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DualCameraApp()
    window.show()
    sys.exit(app.exec())
