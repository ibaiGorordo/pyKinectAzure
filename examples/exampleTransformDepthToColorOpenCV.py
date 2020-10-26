import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll' 
# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Modify camera configuration
	device_config = pyK4A.config
	device_config.color_format = _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_720P
	device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
	print(device_config)

	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)

	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the depth image from the capture
		depth_image_handle = pyK4A.capture_get_depth_image()

		# Get the color image from the capture
		color_image_handle = pyK4A.capture_get_color_image()

		# Check the image has been read correctly
		if depth_image_handle and color_image_handle:

			# Read and convert the image data to numpy array:
			color_image = pyK4A.image_convert_to_numpy(color_image_handle)[:,:,:3]

			# Transform the depth image to the color format
			transformed_depth_image = pyK4A.transform_depth_to_color(depth_image_handle,color_image_handle)

			# Convert depth image (mm) to color, the range needs to be reduced down to the range (0,255)
			transformed_depth_color_image = cv2.applyColorMap(np.round(transformed_depth_image/30).astype(np.uint8), cv2.COLORMAP_JET)

			# Add the depth image over the color image:
			combined_image = cv2.addWeighted(color_image,0.7,transformed_depth_color_image,0.3,0)
			
			# Plot the image
			cv2.namedWindow('Colorized Depth Image',cv2.WINDOW_NORMAL)
			cv2.imshow('Colorized Depth Image',combined_image)
			k = cv2.waitKey(25)

			pyK4A.image_release(depth_image_handle)
			pyK4A.image_release(color_image_handle)

		pyK4A.capture_release()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()