import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Modify camera configuration
	device_config = pyKinectAzure.config()
	device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
	print(device_config)

	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)

	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the color image from the capture
		depth_image = pyK4A.capture_get_depth_image()

		# Check the image has been read correctly
		if depth_image:

			# Read and convert the image data to numpy array:
			imageMat = pyK4A.image_convert_to_numpy(depth_image)

			# Plot the image
			cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)
			cv2.imshow("Color Image",imageMat)
			k = cv2.waitKey(20)

			# Release the image
			pyK4A.image_release(depth_image)

		pyK4A.capture_release()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()