from cv2studio import App, Component, TrackBar, VIDEO
from cv2studio.components import *
import cv2


class ToGrayConversion(Component):
    def process(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img


class BGRRequiredConversion(Component):
    def process(self, img):
        if img.shape[-1] != 3:
            print("Assertion caught!")
            raise AssertionError("Image should be in bgr format!")
        return img


class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        self.add_component(ToGrayConversion())
        self.add_component(BGRRequiredConversion())


app = VideoApp('../res/forest.mp4')
app.main_loop()
