"""
The main example of the framework.
Here is shown how to use component-based
programming with cv2studio.
"""
from cv2studio import App, Component, TrackBar, VIDEO
from cv2studio.components import *
import cv2


class Blur(Component):
    """
    Component to blur an image.
    """
    def __init__(self):
        """
        While initialization you should specify all
        necessary data and also track bars to control
        actions of the component.
        """
        self.track_ksize = TrackBar(min_value=1, max_value=100, start_value=1, step=2)

    def process(self, img):
        """
        Here you specify image processing routine.
        """
        ksize = self.track_ksize.get_value()
        img = cv2.GaussianBlur(img, (ksize, ksize), 5)
        return img


class VideoApp(App):
    def __init__(self, path):
        # Base class initialization is required
        App.__init__(self, path, VIDEO)

        # Adding components to the application
        self.add_component(Blur())

    def pre_process(self, img):
        # This method will be called
        # before any component
        print('Pre-processing...')
        return img

    def post_process(self, img):
        # This method will be called
        # after all component
        print('Post-processing...')
        return img


# Create application for the specified video
# and run it.
app = VideoApp('../res/forest.mp4')
app.main_loop()
