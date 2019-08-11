from .component import Component
import cv2


class GaussianBlur(Component):
    default_ksize = (5, 5)
    default_sigmaX = 3

    def __init__(self, **kwargs):
        Component.__init__(self)

        # extracting attributes
        ksize = kwargs.get('ksize', GaussianBlur.default_ksize)
        sigmaX = kwargs.get('sigmaX', GaussianBlur.default_sigmaX)

        self.state['ksize'] = ksize
        self.state['sigmaX'] = sigmaX

    def process(self, img):
        result = cv2.GaussianBlur(img, self.state['ksize'], self.state['sigmaX'])
        return result
