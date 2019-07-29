from cv2studio import App, Component, TrackBar, VIDEO
from cv2studio.components import *
import cv2


class Blur(Component):
    def __init__(self):
        self.track_ksize = TrackBar(min_value=1, max_value=100, start_value=1, step=2)

    def process(self, img):
        ksize = self.track_ksize.get_value()
        img = cv2.GaussianBlur(img, (ksize, ksize), 5)
        return img


class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        # self.add_component(MyComponent())
        self.add_component(Blur())

    # def pre_process(self, img):
    #     # some manipulations with the image
    #     return img
    #
    # def post_process(self, img):
    #     # some manipulations with the image
    #     return img


app = VideoApp('../res/forest.mp4')
app.main_loop()
