import cv2
import pickle


class ComponentState:
    """
    Holds state of the component
    used by processing method.
    """
    def __init__(self, state_dict=None):
        self.__state = dict() if state_dict is None else state_dict

    def load(self, path: str):
        """
        Loads a component state from a drive
        :param path: path to a pickle file where a component is stored
        :return: None
        """
        with open(path, 'br') as f:
            self.__state = pickle.load(f)

    def save(self, path: str):
        """
        Saves a component
        :param path: path where to save a component
        :return: None
        """
        with open(path, 'bw') as f:
            pickle.dump(self.__state, f)
            
    def __getitem__(self, item):
        if item in self.__state:
            return self.__state[item]
        else:
            return None

    def __setitem__(self, key, value):
        self.__state[key] = value


class Component(object):
    """
    Component is a part of image processing app.
    """
    def __call__(self, img):
        """
        Additional proxy layer between
        application and component.
        :param img: image to process
        :return: processed image
        """

        # auto layer tuning
        # Supported formats
        # - BGR
        # - GRAY
        try:
            result = self.process(img)
        except Exception:
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif len(img.shape) == 2:
                img = cv2.merge((img, img, img))
            result = self.process(img)

        return result

    def process(self, img):
        """
        Core of a component.This method must be
        implemented in a child-class.
        :param img: image to be precessed
        :return: processed image
        """
        raise NotImplementedError('process(img) is not implemented.')