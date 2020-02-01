import cv2studio
import cv2studio.components as components
import cv2


class VideoApp(cv2studio.App):
    def __init__(self, path):
        cv2studio.App.__init__(self, path, cv2studio.VIDEO)


app = VideoApp('../res/forest.mp4')
app.main_loop()
