# cv2studio

`cv2studio` is an OpenCV framework that give
you an ability to decompose processing flow into
components.

## Features

- Component-based development
- Channel independence 
- Classes wrappers for HighGUI elements of OpenCV
- Channel independence for components

## Getting Started

The main principle behind this framework is decomposition.
Splitting up a code into one-format components make
it highly reusable. It becomes easy to develop
different parts of video/image processing separately and
share it with others.

## Installing

To install the current release:
```
pip install cv2studio
```

## Examples

#### Importing
Before using features of the framework
goes importing.

`from cv2studio import App, Component`

#### Component creation

To create a component describe a class derived from `Component`.
To use this class it's required to declare the method `process(self, img)`,
where `img` is an image to be process. This function must return an image as well.

```python
class Blur(Component):
    def process(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 5)
        return img
```

This component apply blur to an input image.

#### App creation

To create an app that will hold processing components
describe a class derived from 'App' and add components
using `add_component(component)` method.

```python
class VideoApp(App):
    def __init__(self, path):
        App.__init__(self, path, VIDEO)
        # self.add_component(MyComponent())
        self.add_component(Blur())
```

#### Running
To run the described app use `main_loop` method.
It will start main processing loop with applying
chain of added component.

```python
app = VideoApp('path/to/video')
app.main_loop()
```

`main_loop` starts a video processing loop. For creating
more complex app see the following examples.


## Testing

To run tests run the following command:

```
pytest
```

## Versioning

We use SemVer for versioning. For the versions available,
see the tags on this repository.

## Contributing

Please read CONTRIBUTE.md for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.txt) file for details

