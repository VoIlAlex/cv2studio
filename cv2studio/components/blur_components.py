from .component import Component
import cv2


class GaussianBlur(Component):
    def __init__(self):
        Component.__init__(self)
        self.state['ksize'] = (5, 5)
        self.state['sigmaX'] = 3

    def process(self, img):
        result = cv2.GaussianBlur(img, self.state['ksize'], self.state['sigmaX'])
        return result
