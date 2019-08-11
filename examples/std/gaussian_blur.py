from cv2studio import App, Component, VIDEO
from cv2studio.components import *
import cv2


class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        # self.add_component(MyComponent())
        self.add_component(GaussianBlur())

    # def pre_process(self, img):
    #     # some manipulations with the image
    #     return img
    #
    # def post_process(self, img):
    #     # some manipulations with the image
    #     return img


app = VideoApp('../../res/forest.mp4')
app.main_loop()
