import cv2
from numpy.random import randint as rand
import imutils
import numpy as np

# TODO: refactor the src (write documentation, remove redundancy, etc.)

'''
Summary:

TrackBar

    Description: Use this for creating new track bar

WindowBase

    Description: Base class for all the windows

TrackWindow

    Description: Window that contains track bars

LogWindow

    Description: Window for logging
'''

__all__ = [
    'TrackBar',
    'TrackWindow',
    'Window',
    'LogWindow',
    'default_window_for_track_bars'
]

# this window will contain all the track bars we create
# type - TrackWindow
# it is initialised when you create first track bar
# or you can initialize it manually
default_window_for_track_bars = None

# these guys is used when you create unnamed
# window / track bar / text window / track bar window
track_bars_count = 0
track_bar_windows_count = 0
windows_count = 0
text_windows_count = 0


class TrackBar:
    # This function is used by track bar (as onChange parameter)
    def __routine(self, x):
        # step is the difference between two values
        # e. g. 1, 3, 5 for step 2
        #       1, 2, 3 for step 1 (default)
        min_value_diff = x - self.min_value
        if min_value_diff % self.step == 0:
            pass
        else:
            potential_value_1 = x - min_value_diff % self.step + self.step
            potential_value_2 = x - min_value_diff % self.step
            if potential_value_1 < self.max_value:
                self.set(potential_value_1)
            else:
                self.set(potential_value_2)

        # calling the user specified routine
        if self.on_change and callable(self.on_change):
            self.on_change(x)

    def __init__(self, name='Track', min_value=0, max_value=10, start_value=None, step=1, on_change=None, parent=None):
        global track_bars_count
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
        if default_window_for_track_bars and parent is None:
            default_window_for_track_bars.append_track_bar(self)
        elif parent is not None:
            parent.append_track_bar(self)

    def display(self):
        if self.displayed is False:
            cv2.createTrackbar(self.name, self.parent_window.window_name, self.start_value, self.max_value,
                               self.__routine)
            cv2.setTrackbarMin(self.name, self.parent_window.window_name, self.min_value)
            self.displayed = True

    def get_value(self):
        if self.parent_window is None:
            return -1
        return cv2.getTrackbarPos(self.name, self.parent_window.window_name)

    def set(self, value):
        if self.parent_window is None:
            return -1
        cv2.setTrackbarPos(self.name, self.parent_window.window_name, value)


class WindowBase:
    def __init__(self, window_name: str, width=600, height=400):
        self.window_name = window_name
        self.displayed = False
        self.width = width
        self.height = height

        self.init_width = width
        self.tracks = []

    def display(self):
        self.displayed = True
        for track in self.tracks:
            track.display()

    def hide(self):
        if self.displayed is True:
            try:
                cv2.destroyWindow(self.window_name)
            except Exception:
                pass
        self.displayed = False

    def append_track_bar(self, track: TrackBar):
        self.tracks.append(track)
        track.parent_window = self


class TrackWindow(WindowBase):
    def __init__(self, window_name: str = 'Track bars'):
        global track_bar_windows_count, default_window_for_track_bars
        if window_name == 'Track bars':
            window_name += str(track_bar_windows_count)
            track_bar_windows_count += 1
        super().__init__(window_name)
        self.tracks = []
        if default_window_for_track_bars is None:
            default_window_for_track_bars = self

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

