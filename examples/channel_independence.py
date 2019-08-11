from cv2studio import App, Component, TrackBar, VIDEO
from cv2studio.components import *
import cv2


class ToGrayConversion(Component):
    def process(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img


class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        # self.add_component(MyComponent())
        self.add_component(ToGrayConversion())

    # def pre_process(self, img):
    #     # some manipulations with the image
    #     return img
    #
    # def post_process(self, img):
    #     # some manipulations with the image
    #     return img


app = VideoApp('../res/forest.mp4')
app.main_loop()
