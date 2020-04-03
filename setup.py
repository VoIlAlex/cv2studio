from distutils.core import setup
from setuptools import find_packages
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='cv2studio',
    packages=find_packages('.'),
    version='1.0.2',
    license='MIT',
    description='Chain-based framework to split image processing into components.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ilya Vouk',
    author_email='ilya.vouk@gmail.com',
    url='https://github.com/VoIlAlex/cv2studio',
    download_url='https://github.com/VoIlAlex/cv2studio/archive/1.0.2.tar.gz',
    keywords=['OpenCV', 'Computer Vision',
              'Framework', 'Wrapper', 'Components'],
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
