# pyKinectAzure

![Azure kinect color and depth combination](https://github.com/ibaiGorordo/pyKinectAzure/blob/master/doc/images/Azure%20kinect%20depth%20and%20color%20combination.png)

This complete library in Python 3 for the Azure-Kinect-Sensor-SDK.

## Similar solutions
Part of the ideas in this repository are taken from following repositories:
* [pyk4a](https://github.com/etiennedub/pyk4a): Really nice and clean Python3 wrapper for the Kinect Azure SDK. Some features are still lacking such as inertial sensor data acquisition, skeleton tracking...

* [Azure-Kinect-Python](https://github.com/hexops/Azure-Kinect-Python): More complete library using ctypes as in this repository, however, examples about how to use the library are missing and the library is harder to use.

The objective of this repository is to combine the strong points of both repositories by creating a easy to use library that allows the use of most of the functions of the Kinect Azure. Also, to create sample programs to showcase the uses of the library

## Prerequisites
* [Azure-Kinect-Sensor-SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK): required to build this library.
  To use the SDK, refer to the installation instructions [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK).
* **ctypes**: required to read the library.
* **numpy**: required for the matrix calculations
* **opencv-python**: Required for the image transformations and visualization.

## How to use this library
* The library has **only been tested in Windows** with the Kinect Azure SDK 1.4.0, it should also work with other operating systems.

* When using the pyKinectAzure class, it requires the **path to the k4a.dll module**, make sure that the path is the correct one for your Kinect Azure SDK version. By default the path is set to  ```C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll```.

* The **pyKinectAzure** class is a wrapper around the **_k4a.py** module to make the library more understandable. However, the **pyKinectAzure** class still contains few methods from the Kinect Azure SDK

* The **_k4a.py** module already contains all the methods in the Kinect Azure SDK. So, for more advanced of the Kinect Azure SDK check the **_k4a.py** module.




## Example

For an example on how to obtain and visualize the video from the Kinect Azure check the **exampleColorImageOpenCV.py** script.

```
git clone https://github.com/ibaiGorordo/pyKinectAzure.git
cd pyKinectAzure/examples
python exampleColorImageOpenCV.py
```

## Contribution

Feel free to send pull requests.

Bug reports are also appreciated. Please include as much details as possible.

## TODO:

### Wrappers for the Kinect Azure data
- [x] Create wrapper to read depth images.
- [x] Create wrapper to read Infrared images.
- [x] Create wrapper to read IMU data.
- [x] Create function to convert image buffer to image depending on the image type.
- [x] Create wrapper to transform depth image to color image.
- [ ] Create wrapper to transform depth image to 3D point cloud.
- [ ] Create funtion to visualize 3D point cloud.

### Create examples
- [x] Example to visualize depth images.
- [x] Example to visualize passive IR images.
- [x] Example to plot IMU data.
- [x] Example to visualize Depth as color image.
- [x] Example to overlay depth color with alpha over real image.
- [ ] Example to visualize 3D point cloud

### Body tracking
- [ ] Create library for the body tracking SDK similar the same way as the current library.
- [ ] Combine image and skeleton data.
- [ ] Generate 3D skeleton visualization.

### Future ideas
- [ ] Run Deep Learning models on Kinect data (Openpose 3D skeleton, semantic segmentation with depth, monocular depth estimation validation)
- [ ] Track passive infrared marker for motion capture analysis
