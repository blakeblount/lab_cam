import sys
import cv2
from datetime import datetime
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QGridLayout, QPushButton, QVBoxLayout, QGroupBox, QCheckBox

class Pentopticon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pentopticon")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.active_camera_groupbox = QGroupBox("Active Cameras", self)

        self.active_camera_groupbox_layout = QVBoxLayout(self.active_camera_groupbox)

        self.camera_0_checkbox = QCheckBox("Camera 0")
        self.camera_1_checkbox = QCheckBox("Camera 1")

        self.active_camera_groupbox_layout.addWidget(self.camera_0_checkbox)
        self.active_camera_groupbox_layout.addWidget(self.camera_1_checkbox)

        self.layout.addWidget(self.active_camera_groupbox)

        self.camera_0_checkbox.toggled.connect(self.toggle_camera_0_streaming)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.label_cam0 = QLabel(self)
        self.label_cam1 = QLabel(self)

        self.grid_layout.addWidget(self.label_cam0, 0, 0)
        self.grid_layout.addWidget(self.label_cam1, 0, 1)

        self.record_button = QPushButton("Start Recording", self)
        self.layout.addWidget(self.record_button)
        self.record_button.clicked.connect(self.toggle_recording)

        self.camera_0_is_streaming = False
        self.camera_1_is_streaming = False
        self.camera_0 = None
        self.camera_1 = None

#        self.cam0 = cv2.VideoCapture(0)
        self.cam1 = cv2.VideoCapture(1)

        self.is_recording = False
        self.out0 = None
        self.out1 = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def toggle_camera_0_streaming(self):
        if self.camera_0_is_streaming:
            self.camera_0_is_streaming = False
            self.stop_camera_0_streaming()
        else:
            self.camera_0_is_streaming = True
            self.start_camera_0_streaming()


    def start_camera_0_streaming(self):
        self.camera_0 = cv2.VideoCapture(0)

    def stop_camera_0_streaming(self):
        self.camera_0.release()

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.record_button.setText("Start Recording")
            self.stop_recording()
        else:
            self.is_recording = True
            self.record_button.setText("Stop Recording")
            self.start_recording()

    def start_recording(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out0 = cv2.VideoWriter('camera_0_output.avi', fourcc, 30.0, (640, 480))
        self.out1 = cv2.VideoWriter('cam_1_output.avi', fourcc, 30.0, (640, 480))

    def stop_recording(self):
        if self.out0 is not None:
            self.out0.release()
        if self.out1 is not None:
            self.out1.release()

    def update_frame(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

        if self.camera_0_is_streaming:
            ret0, frame0 = self.camera_0.read()

            if ret0:
                cv2.putText(frame0, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                if self.is_recording:
                    self.out0.write(cv2.cvtColor(frame0, cv2.COLOR_RGB2BGR))

                    cv2.circle(frame0, (610, 23), 15, (0, 0, 255), -1)

                frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)

                qimg0 = QImage(frame0.data, frame0.shape[1], frame0.shape[0], QImage.Format.Format_RGB888)

                self.label_cam0.setPixmap(QPixmap.fromImage(qimg0))



        ret1, frame1 = self.cam1.read()

        if ret1:

            cv2.putText(frame1, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            if self.is_recording:
                self.out1.write(cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))

                cv2.circle(frame1, (610, 23), 15, (0, 0, 255), -1)

            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

            qimg1 = QImage(frame1.data, frame1.shape[1], frame1.shape[0], QImage.Format.Format_RGB888)

            self.label_cam1.setPixmap(QPixmap.fromImage(qimg1))

    def closeEvent(self, event):
        self.cam0.release()
        self.cam1.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = Pentopticon()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

