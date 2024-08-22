import sys
import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QGridLayout

class Pentopticon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pentopticon")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        #self.layout = QHBoxLayout(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        self.label_cam0 = QLabel(self)
        self.label_cam1 = QLabel(self)

        #self.layout.addWidget(self.label_cam0)
        #self.layout.addWidget(self.label_cam1)
        self.layout.addWidget(self.label_cam0, 0, 0)
        self.layout.addWidget(self.label_cam1, 0, 1)

        self.cam0 = cv2.VideoCapture(0)
        self.cam1 = cv2.VideoCapture(1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def update_frame(self):
        ret0, frame0 = self.cam0.read()
        ret1, frame1 = self.cam1.read()

        if ret0 and ret1:
            frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

            qimg0 = QImage(frame0.data, frame0.shape[1], frame0.shape[0], QImage.Format.Format_RGB888)
            qimg1 = QImage(frame1.data, frame1.shape[1], frame1.shape[0], QImage.Format.Format_RGB888)

            self.label_cam0.setPixmap(QPixmap.fromImage(qimg0))
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

