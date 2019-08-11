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
        result = cv2.GaussianBlur(img,
                                  self.state['ksize'],
                                  self.state['sigmaX'])
        return result


class BilateralBlur(Component):
    default_d = 9
    default_sigmaColor = 75
    default_sigmaSpace = 75

    def __init__(self, **kwargs):
        Component.__init__(self)

        # extracting attributes
        d = kwargs.get('d', BilateralBlur.default_d)
        sigmaColor = kwargs.get('sigmaColor', BilateralBlur.default_sigmaColor)
        sigmaSpace = kwargs.get('sigmaSpace', BilateralBlur.default_sigmaSpace)

        self.state['d'] = d
        self.state['sigmaColor'] = sigmaColor
        self.state['sigmaSpace'] = sigmaSpace

    def process(self, img):
        result = cv2.bilateralFilter(img,
                                     self.state['d'],
                                     self.state['sigmaColor'],
                                     self.state['sigmaSpace'])
        return result