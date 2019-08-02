"""
    This module contains graphic user interface
    utilities for the cv2studio framework.
"""

import cv2
from numpy.random import randint as rand
import imutils
import numpy as np

# TODO: refactor the src (write documentation, remove redundancy, etc.)

__all__ = [
    'TrackBar',
    'TrackWindow',
    'LogWindow',
    'Window',
    'default_track_window'
]

# this window will contain all the track bars we create
# type - TrackWindow
# it is initialised when you create first track bar
# or you can initialize it manually
default_track_window = None

# these guys is used when you create unnamed
# window / track bar / text window / track bar window
# to count already created units
track_bars_count = 0
track_bar_windows_count = 0
windows_count = 0
text_windows_count = 0


class TrackBar:
    # TODO: hide method
    """
        Class wrapper for cv2 track bar.

        Does not require window creation.
        If parent window is not specified
        then default window used instead.
        If there is no default window then
        one is created.

        To define onChange function-handler
        assign it to <on_change> attribute.
        It's called inside __routine method.
    """

    def __init__(self, name='Track', min_value=0, max_value=10, start_value=None, step=1, on_change=None, parent=None):
        global track_bars_count, default_track_window

        # Generation of unique default
        # name for the track bar if necessary
        if name == 'Track':
            name += str(track_bar_windows_count)
            track_bars_count += 1
        self.name = name

        self.min_value = min_value
        self.max_value = max_value
        self.start_value = start_value if start_value is not None else rand(min_value, max_value)
        self.step = step
        self.on_change = on_change
        self.parent_window = parent
        self.displayed = False

        # bounding with the parent window
        if default_track_window is None:
            default_track_window = TrackWindow()
        if self.parent_window is None:
            self.parent_window = default_track_window
        self.parent_window.append_track_bar(self)

    def display(self):
        """
        Displays the track bar. It's called by
        display method of parent window of the track bar.
        :return:
        """
        if self.displayed is False:
            cv2.createTrackbar(self.name, self.parent_window.window_name, self.start_value, self.max_value,
                               self.__routine)
            cv2.setTrackbarMin(self.name, self.parent_window.window_name, self.min_value)
            self.displayed = True

    def get_value(self):
        """
        Used to access the position of the track bar
        :return: current position of the track bar
        """
        if self.parent_window is None:
            return -1
        return cv2.getTrackbarPos(self.name, self.parent_window.window_name)

    def set_value(self, value):
        """
        Sets position of the track bar.
        :param value: required position of track bar
        :return: if success - True, if fail - False
        """
        if self.parent_window is None:
            return False
        cv2.setTrackbarPos(self.name, self.parent_window.window_name, value)
        return True

    def __routine(self, x):
        """
        This function is used by track bar as onChange parameter.
        It serves as proxy that intercept call to user defined
        method for accomplish features like step implementation.
        :param x: track position. It's passed by OpenCV.
        :return: None
        """

        # step implementation
        relative_position = x - self.min_value
        if relative_position % self.step == 0:
            pass
        else:
            potential_value_high = x - relative_position % self.step + self.step
            potential_value_low = x - relative_position % self.step
            if potential_value_high < self.max_value:
                self.set_value(potential_value_high)
            else:
                self.set_value(potential_value_low)

        # calling the user specified routine
        if self.on_change and callable(self.on_change):
            self.on_change(x)


class WindowBase:
    """
    Base class for all window classes
    of the frame work. Contains overridable routines
    for displaying and hiding window.
    """
    def __init__(self, window_name: str, width=600, height=400):
        self.window_name = window_name
        self.displayed = False
        self.width = width
        self.height = height
        self.tracks = []

    def display(self):
        """
        Displays window and all attached
        track bars.
        :return: None
        """
        self.displayed = True
        for track in self.tracks:
            track.display()

    def hide(self):
        """
        Destroys the window.
        :return: None
        """
        if self.displayed is True:
            try:
                cv2.destroyWindow(self.window_name)
            # TODO: what kind of exception does it throw when there is no such a window
            except Exception:
                pass
        self.displayed = False

    def append_track_bar(self, track: TrackBar):
        """
        Sets correlations between the track bar
        and the window. So that window will be able
        to display it in the future.
        :param track:
        :return:
        """
        self.tracks.append(track)
        track.parent_window = self


class TrackWindow(WindowBase):
    def __init__(self, window_name: str = 'Track bars'):
        global track_bar_windows_count, default_track_window
        if window_name == 'Track bars':
            window_name += str(track_bar_windows_count)
            track_bar_windows_count += 1
        super().__init__(window_name)
        self.tracks = []
        if default_track_window is None:
            default_track_window = self

    def display(self):
        if not self.displayed:
            cv2.namedWindow(self.window_name)
        super().display()

    def append_track_bar(self, track: TrackBar):
        self.tracks.append(track)
        track.parent_window = self
        if not self.displayed:
            self.display()
        else:
            track.display()


class LogWindow(WindowBase):
    def __init__(self, window_name='WindowText', width=600, height=400):
        global text_windows_count
        if window_name == 'WindowText':
            window_name += str(text_windows_count)
            text_windows_count += 1
        super().__init__(window_name, width, height)
        self.window_area = np.zeros(shape=(height, width), dtype='uint8')
        self.text = {}

    def display(self):
        result = self.window_area.copy()
        character_height = 20
        row_length = self.width // 10
        line_idx = 0
        for key, value in self.text.items():
            text = '{0}: {1}'.format(key, value)
            text = text.split('\n')
            # split text into lines so that
            # they fit for displaying
            i = 0
            while i != len(text):
                if len(text[i]) > row_length:
                    text = text[:i] + [text[i][0:row_length], text[i][row_length:]] + text[i + 1:]
                i += 1
            # print each line on a new line
            for line in text:
                cv2.putText(result, line, (10, character_height * (line_idx + 1)), cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (255, 255, 255), 1, cv2.LINE_AA)
                line_idx += 1

        cv2.imshow(self.window_name, result)
        super().display()

    def __getitem__(self, item):
        return self.text[item]

    def __setitem__(self, key, value):
        self.text[key] = str(value)

    def set_from_dict(self, dict_to_display: dict):
        for key in dict_to_display:
            self[key] = dict_to_display[key]


class Window(WindowBase):
    def __init__(self, window_name='Window', width=None):
        global windows_count
        if window_name == 'Window':
            if windows_count > 0:
                window_name += str(windows_count)
            windows_count += 1
        window_name = str(window_name)
        super().__init__(window_name, width)
        self.attached_track_windows = []

    def imshow(self, img):
        if self.width is not None:
            img = imutils.resize(img, width=self.width)
        cv2.imshow(self.window_name, img)
        for track_window in self.attached_track_windows:
            if not track_window.displayed:
                track_window.display()
        super().display()

    def attach_track_window(self, track_window: TrackWindow):
        self.attached_track_windows.append(track_window)
