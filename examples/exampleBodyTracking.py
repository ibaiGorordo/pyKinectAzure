import sys

from model.Joint import Joint
from model.BodyKeyPoints import BodyKeyPoint
from typing import NamedTuple

from model.joint2D import Joint2D
from processor.Drawer import Drawer

sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from typing import List
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

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

	# Initialize the body tracker
	pyK4A.bodyTracker_start(bodyTrackingModulePath)

	k = 0
	while True:
		# Get capture
		keypoint_list: List[Joint] = []
		modify_keypoint_list: List[Joint2D] = []
		pyK4A.device_get_capture()

		# Get the depth image from the capture
		depth_image_handle = pyK4A.capture_get_depth_image()


		# Check the image has been read correctly
		if depth_image_handle:

			# Perform body detection
			pyK4A.bodyTracker_update()

			# Get the information of each body
			for body in pyK4A.body_tracker.bodiesNow:
				for bodyKeyPoint in BodyKeyPoint:
					keypoint_list.append(pyK4A.body_tracker.getBodyPosition(body, bodyKeyPoint))

			if len(keypoint_list) != 0:
				print(keypoint_list)
				for joint in keypoint_list:
					after_joint = pyK4A.get_k4a_calibration_3d_to_2d(joint)
					modify_keypoint_list.append(after_joint)

			# Read and convert the image data to numpy array:
			depth_image = pyK4A.image_convert_to_numpy(depth_image_handle)
			depth_color_image = cv2.convertScaleAbs (depth_image, alpha=0.05)  #alpha is fitted by visual comparison with Azure k4aviewer results
			depth_color_image = cv2.cvtColor(depth_color_image, cv2.COLOR_GRAY2RGB)

			depth_color_image = Drawer.draw_circle_on_image(depth_color_image, modify_keypoint_list)
			# Get body segmentation image
			# body_image_color = pyK4A.bodyTracker_get_body_segmentation()

			# combined_image = cv2.addWeighted(depth_color_image, 0.8, body_image_color, 0.2, 0)

			# Overlay body segmentation on depth image
			cv2.imshow('Segmented Depth Image', depth_color_image)
			k = cv2.waitKey(1)
			# Release the image
			pyK4A.image_release(depth_image_handle)
			pyK4A.image_release(pyK4A.body_tracker.segmented_body_img)

		pyK4A.capture_release()
		pyK4A.body_tracker.release_frame()

		if k==27:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()
