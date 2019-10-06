'''
    This is the cv2 framework. Using this
    framework it becomes easier to decompose
    an image processing app into components.
'''
import cv2
from .gui import *

# constants for path type
WEBCAM = 0
IMAGE = 1
VIDEO = 2
RESOURCE = 3


class Component(object):
    '''
    Component is a part of image processing app.
    '''

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
        '''
        Core of a component. This method must be
        implemented in a child-class.
        :param img: image to be precessed
        :return: processed image
        '''
        raise NotImplementedError('process(img) is not implemented.')


# TODO: FPS adjustment so user can set it.
# TODO: optional width and height for App
# TODO: automatic resource type recognition
class App(object):
    def __init__(self, path: str = None, resource_type=WEBCAM, window_name='Window', resource=None):
        '''
        :param path: path to resource (image or video)
        :param resource_type: type of resource (WEBCAM, IMAGE, VIDEO)
        :param window_name: name of the application's main window
        '''

        # image to be shown
        self.img = None

        self.resource_type = resource_type
        if resource_type == WEBCAM:
            self.res = cv2.VideoCapture(0)
        elif resource_type == VIDEO:
            self.res = cv2.VideoCapture(path)
        elif resource_type == IMAGE:
            self.res = cv2.imread(path)
        elif resource_type == RESOURCE:
            self.res = resource

        # verify resource
        if self.res is None:
            raise AttributeError('failed to load a resource {}'.format(path))
        if self.resource_type == VIDEO:
            _, test_frame = self.res.read()
            if test_frame is None:
                raise AttributeError(
                    'failed to load a resource {}'.format(path))

        # components are parts
        # image processing
        self.components = []

        # window for processed frame
        self.window = Window(window_name)

        # window that will keep
        # track bars
        self.tracks_window = TrackWindow()

    def add_component(self, component: Component):
        self.components.append(component)

        # add track bars from
        # component to track bar
        # holding window
        for attr in component.__dict__.values():
            if isinstance(attr, TrackBar):
                self.tracks_window.append_track_bar(attr)

    def pre_process(self, img):
        '''
        This method is called before any components.
        It must be overridden if pre-processing is
        required.
        :param img: image to be processed
        :return: processed image
        '''
        return img

    def post_process(self, img):
        '''
        This method is called after all components.
        It must be overridden if post-processing is
        required.
        :param img: image to be processed
        :return: processed image
        '''
        return img

    def update(self):
        '''
        When this method is called one iteration of
        processing is performed.
        :return: None
        '''
        # getting image from resource
        img = None
        if self.resource_type == VIDEO or self.resource_type == WEBCAM:
            result, img = self.res.read()

        elif self.resource_type == IMAGE:
            img = self.res.copy()
            result = True

        # Here is where image processing go
        img = self.pre_process(img)
        for component in self.components:
            img = component(img)
        img = self.post_process(img)

        self.img = img
        return result

    def display(self):
        if self.img is not None:
            self.window.imshow(self.img)
        else:
            self.window.hide()
            self.tracks_window.hide()
        self.tracks_window.display()

    def main_loop(self, **kwargs):
        '''
        This method starts main loop of
        processing.
        :return: None
        :keyword delay: defines delay for each iteration.
        '''

        # extracting arguments
        delay = kwargs.get('delay', 10)

        # processing
        while self.update():

            # The display command
            # displays results of the
            # processing as well as
            # hides windows in the end
            self.display()
            key = cv2.waitKey(delay)
            if key == ord('q'):
                break

        # cleaning up
        if self.resource_type == VIDEO or self.resource_type == WEBCAM:
            self.res.release()

        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = App('/home/ilya/Documents/Code/py/cv2studio/res/slp.mp4', VIDEO)
    app.main_loop()
