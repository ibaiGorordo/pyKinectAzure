
import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
from kinectBodyTracker import kinectBodyTracker, _k4abt
import cv2

colors = np.ones((256,4), dtype=np.uint8)
colors[:3,:] = np.array([[202, 183, 42, 255], [42, 202, 183, 255], [183, 42, 202, 255]]) 

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll' 
bodyTrackingModulePath = 'C:\\Program Files\\Azure Kinect Body Tracking SDK\\sdk\\windows-desktop\\amd64\\release\\bin\\k4abt.dll'
# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Modify camera configuration
	device_config = pyK4A.config
	device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_OFF
	device_config.depth_mode = _k4a.K4A_DEPTH_MODE_NFOV_UNBINNED
	print(device_config)

	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)

	# Get depth sensor calibration
	depthSensorCalibration = _k4a.k4a_calibration_t()
	pyK4A.getDepthSensorCalibration(depthSensorCalibration)

	# Initialize the body tracker
	pyK4ABT = kinectBodyTracker(bodyTrackingModulePath, depthSensorCalibration)

	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the depth image from the capture
		depth_image_handle = pyK4A.capture_get_depth_image()

		# Add capture to the body tracker processing queue
		pyK4ABT.enqueue_capture(pyK4A.capture_handle)

		# Check the image has been read correctly
		if depth_image_handle:

			pyK4ABT.detectBodies()

			# Read and convert the image data to numpy array:
			depth_image = pyK4A.image_convert_to_numpy(depth_image_handle)
			depth_color_image = cv2.convertScaleAbs (depth_image, alpha=0.05)  #alpha is fitted by visual comparison with Azure k4aviewer results 
			depth_color_image = cv2.cvtColor(depth_color_image, cv2.COLOR_GRAY2RGB) 

			body_image = pyK4A.image_convert_to_numpy(pyK4ABT.segmented_body_img).astype(np.uint8)
			body_image_color = np.dstack([cv2.LUT(body_image, colors[:,i]) for i in range(3)])

			combined_image = cv2.addWeighted(depth_color_image, 0.5, body_image_color, 0.5, 0)

			# Overlay body segmentation on depth image
			cv2.imshow('Segmented Depth Image',combined_image)
			k = cv2.waitKey(1)

			# Release the image
			pyK4A.image_release(depth_image_handle)
			pyK4A.image_release(pyK4ABT.segmented_body_img)

		pyK4A.capture_release()
		pyK4ABT.release_frame()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()
