import sys
import os
import importlib


def import_cv2studio():
    root_dir = os.path.sep.join(__file__.split(os.path.sep)[:-2])
    sys.path.insert(0, root_dir)
    import cv2studio
    return cv2studio


cv2studio = import_cv2studio()


class TestTrackBar:
    def test_default(self):
        track_bar = cv2studio.TrackBar('Track', 0, 100, 20)
        assert track_bar.get_value() == 20

    def test_get_set(self):
        track_bar = cv2studio.TrackBar('Track', 0, 100, 20)
        track_bar.set_value(50)
        assert track_bar.get_value() == 50

    def test_max_value(self):
        track_bar = cv2studio.TrackBar('Track', 0, 100, 20)
        track_bar.set_value(110)
        assert track_bar.get_value() == 100

    def test_min_value(self):
        track_bar = cv2studio.TrackBar('Track', 0, 100, 20)
        track_bar.set_value(-1)
        assert track_bar.get_value() == 0
