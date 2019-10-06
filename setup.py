from distutils.core import setup

setup(
    name='cv2studio',
    packages=['cv2studio'],
    version='1.0.0-alpha',
    license='MIT',
    description='wrapper for cv2 library that helps to separate different parts of computer vision application',
    author='Ilya Vouk',
    author_email='ilya.vouk@gmail.com',
    url='https://github.com/VoIlAlex/cv2studio',
    download_url='https://github.com/VoIlAlex/cv2studio/archive/1.0.0-alpha.tar.gz',
    keywords=['OpenCV', 'Computer Vision', 'Framework', 'Wrapper'],
    install_requires=[
        'opencv-python',
        'imutils',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ]
)
