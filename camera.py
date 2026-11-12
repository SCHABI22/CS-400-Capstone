#Needs to be converted to OOP
import cv2

class Camera:
    def __init__(self, index=0):
        self.video = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            raise Exception("Error: Could not open video.")
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        for _ in range(10):
            self.video.read()

    def read(self):
        ret, frame = self.video.read()
        if not ret:
            raise Exception("Error: Could not read frame.")
        return frame

    def release(self):
        self.video.release()
        cv2.destroyAllWindows()
