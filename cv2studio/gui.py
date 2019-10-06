"""
    This module contains graphic user interface
    utilities for the cv2studio framework.
"""

import cv2
from numpy.random import randint as rand
import imutils
import numpy as np


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
log_windows_count = 0


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
        self.start_value = start_value if start_value is not None else rand(
            min_value, max_value)
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
            cv2.setTrackbarMin(
                self.name, self.parent_window.window_name, self.min_value)
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

    def __init__(self, window_name: str, width=None, height=None):
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
            cv2.destroyWindow(self.window_name)
        self.displayed = False

    def append_track_bar(self, track: TrackBar):
        """
        Sets correlations between the track bar
        and the window. So that window will be able
        to display it in the future.
        :param track: track bar to attach
        :return: None
        """
        self.tracks.append(track)
        track.parent_window = self


class TrackWindow(WindowBase):
    """
        This kind of window is used to hold
        track bars.
    """

    def __init__(self, window_name: str = 'Track bars'):
        global track_bar_windows_count, default_track_window

        # Generation of unique default
        # name for the track window if necessary
        if window_name == 'Track bars':
            window_name += str(track_bar_windows_count)
            track_bar_windows_count += 1

        if default_track_window is None:
            default_track_window = self

        super().__init__(window_name)

    def display(self):
        """
        Displaying of track window and
        all attacked track bars.
        :return:
        """
        if not self.displayed and len(self.tracks) != 0:
            cv2.namedWindow(self.window_name)
        WindowBase.display(self)

    def append_track_bar(self, track: TrackBar):
        """
        Sets correlations between the track bar
        and the window. So that window will be able
        to display it in the future.
        :param track: track bar to attach
        :return: None
        """
        WindowBase.append_track_bar(self, track)

        if not self.displayed:
            self.display()
        else:
            track.display()


class LogWindow(WindowBase):
    """
    Window used for logging.
    Format of logging:
        log_window[key] = value
    """

    def __init__(self, window_name='WindowText', width=600, height=400):
        global log_windows_count

        # Generation of unique default
        # name for the log window if necessary
        if window_name == 'WindowText':
            window_name += str(log_windows_count)
            log_windows_count += 1

        self.window_area = np.zeros(shape=(height, width), dtype='uint8')
        self.text_to_display = {}

        super().__init__(window_name, width, height)

    def display(self):
        """
        Display all value assigned
        to the internal dictionary.
        :return:None
        """
        area_with_text = self.window_area.copy()
        character_height = 20
        row_length = self.width // 10
        line_idx = 0
        for key, value in self.text_to_display.items():
            text = '{0}: {1}'.format(key, value)

            # if line of the text contains
            # new line characters
            text = text.split('\n')

            # split text into lines so
            # they fit for displaying
            i = 0
            while i != len(text):
                if len(text[i]) > row_length:
                    # split current line
                    # into fitting part
                    # and remainder
                    fitting_part = text[i][0:row_length]
                    remainder = text[i][row_length:]
                    text = text[:i] + [fitting_part, remainder] + text[i+1:]
                i += 1

            # print lines of text
            for line in text:
                cv2.putText(
                    img=area_with_text,
                    text=line,
                    org=(10, character_height * (line_idx + 1)),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255),
                    thickness=1,
                    lineType=cv2.LINE_AA
                )
                line_idx += 1

        cv2.imshow(self.window_name, area_with_text)
        WindowBase.display(self)

    def __getitem__(self, item):
        """
        Used to access item from
        internal dictionary
        :param item: key of item from dictionary
        :return: value of item from dictionary
        """
        return self.text_to_display[item]

    def __setitem__(self, key, value):
        """
        Save item for displaying
        :param key:
        :param value:
        :return: None
        """
        self.text_to_display[key] = str(value)

    def from_dict(self, dict_to_display: dict):
        """
        Updated values in internal
        dictionary by values in passed
        dictionary
        :param dict_to_display: used to update data in internal dictionary
        :return: None
        """
        for key in dict_to_display:
            self[key] = dict_to_display[key]


class Window(WindowBase):
    """
    Window for displaying images.
    """

    def __init__(self, window_name='Window', width=None):
        global windows_count

        # Generation of unique default
        # name for the log window if necessary
        if window_name == 'Window':
            if windows_count > 0:
                window_name += str(windows_count)
            windows_count += 1
        window_name = str(window_name)

        self.attached_track_windows = []
        super().__init__(window_name, width)

    def imshow(self, img):
        """
        Shows an image.
        :param img: image to show
        :return: None
        """

        if self.height is not None or self.width is not None:
            img = imutils.resize(img, width=self.width, height=self.height)
        cv2.imshow(self.window_name, img)

        # displaying bounded track windows
        for track_window in self.attached_track_windows:
            if not track_window.displayed:
                track_window.display()

        WindowBase.display(self)

    def attach_track_window(self, track_window: TrackWindow):
        """
        Saves the track window so that
        it can be displayed with this window.
        :param track_window: track window to save
        :return: None
        """
        self.attached_track_windows.append(track_window)
