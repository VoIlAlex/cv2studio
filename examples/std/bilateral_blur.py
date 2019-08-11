from cv2studio import App, VIDEO
from cv2studio.components import BilateralBlur


class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        # self.add_component(MyComponent())
        self.add_component(BilateralBlur())


app = VideoApp('../../res/forest.mp4')
app.main_loop()
