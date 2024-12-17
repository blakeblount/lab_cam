import cv2
import os
import threading
import time
from datetime import datetime

class MultiCameraFeed:
    def __init__(self, num_cameras):
        self.num_cameras = num_cameras
        self.captures = [cv2.VideoCapture(i, cv2.CAP_DSHOW) for i in range(num_cameras)]
        self.frames = [None] * num_cameras
        self.recording = False
        self.out_writers = [None] * num_cameras
        self.sync_start_time = None

    def _read_frames(self):
        while True:
            for i, cap in enumerate(self.captures):
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        self.frames[i] = frame

    def start_reading(self):
        threading.Thread(target=self._read_frames, daemon=True).start()

    def display_feeds(self):
        while True:
            montage = self._create_montage()
            if montage is not None:
                cv2.imshow('Camera Feeds', montage)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.toggle_recording()

        self.stop()

    def _create_montage(self):
        non_empty_frames = [frame for frame in self.frames if frame is not None]
        if not non_empty_frames:
            return None

        rows = [cv2.hconcat(non_empty_frames[i:i+3]) for i in range(0, len(non_empty_frames), 3)]
        return cv2.vconcat(rows) if rows else None

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.sync_start_time = time.time()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('recordings', exist_ok=True)
        for i, frame in enumerate(self.frames):
            if frame is not None:
                height, width, _ = frame.shape
                out_filename = f'recordings/camera_{i}_{timestamp}.avi'
                self.out_writers[i] = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
        print("Recording started.")

    def stop_recording(self):
        self.recording = False
        for writer in self.out_writers:
            if writer:
                writer.release()
        self.out_writers = [None] * self.num_cameras
        print("Recording stopped.")

    def write_frames(self):
        while True:
            if self.recording:
                for i, writer in enumerate(self.out_writers):
                    if writer and self.frames[i] is not None:
                        timestamp = time.time() - self.sync_start_time
                        cv2.putText(self.frames[i], f"{timestamp:.2f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        writer.write(self.frames[i])

    def stop(self):
        for cap in self.captures:
            if cap.isOpened():
                cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    num_cameras = 2  # Adjust based on available cameras
    multi_cam = MultiCameraFeed(num_cameras)

    multi_cam.start_reading()
    threading.Thread(target=multi_cam.write_frames, daemon=True).start()
    multi_cam.display_feeds()
