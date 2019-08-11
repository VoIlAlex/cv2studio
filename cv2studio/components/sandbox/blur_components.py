from ..component import Component
from ..blur_components import *
from ...gui import *
import cv2


class GaussianBlurSandbox(GaussianBlur):
    def __init__(self, **kwargs):
        GaussianBlur.__init__(self, **kwargs)
        self.ksize_track = TrackBar(name='ksize',
                                    min_value=1,
                                    max_value=100,
                                    start_value=self.state['ksize'][0],
                                    step=2)
        self.sigmaX_track = TrackBar(name='sigmaX',
                                     min_value=0,
                                     max_value=10,
                                     start_value=self.state['sigmaX'],
                                     step=1)

    def process(self, img):
        # getting values from track bars
        ksize_value = self.ksize_track.get_value()
        self.state['ksize'] = (ksize_value, ksize_value)
        self.state['sigmaX'] = self.sigmaX_track.get_value()

        # processing
        img = GaussianBlur.process(self, img)
        result = cv2.GaussianBlur(img,
                                  self.state['ksize'],
                                  self.state['sigmaX'])

        return result
