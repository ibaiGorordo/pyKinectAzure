import sys
sys.path.insert(1, '../src/')

import numpy as np
import _k4atypes as k4atypesk
from pyKinectAzure import pyKinectAzure
import cv2

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Start cameras using default configuration
	pyK4A.device_start_cameras()

	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the color image from the capture
		color_image = pyK4A.capture_get_color_image()

		# Check the image has been read correctly
		if color_image:

			# Get the height and width for the current image:
			color_image_width = pyK4A.image_get_width_pixels(color_image)
			color_image_height= pyK4A.image_get_height_pixels(color_image)

			# Get the pointer to the buffer containing the image data
			imageBuffer = pyK4A.image_get_buffer(color_image)

			# Read the data in the buffer and decode to obtain the image
			jpgArray = np.ctypeslib.as_array(imageBuffer,shape=[color_image_width*color_image_height])
			imageMat = cv2.imdecode(np.frombuffer(jpgArray, dtype=np.uint8), -1)

			# Plot the image
			cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)
			cv2.imshow("Color Image",imageMat)
			k = cv2.waitKey(20)

			# Release the image
			pyK4A.image_release(color_image)

		pyK4A.capture_release()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_close()


