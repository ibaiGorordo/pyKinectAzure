from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pykinect_azure',
    version='0.0.1',
    license='MIT',
    description='Python library to run Kinect Azure DK SDK functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ibai Gorordo',
    url='https://github.com/ibaiGorordo/pyKinectAzure',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
)