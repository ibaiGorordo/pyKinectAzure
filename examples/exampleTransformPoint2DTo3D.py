import cv2

import pykinect_azure as pykinect
from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	# print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	cv2.namedWindow('Transformed Color Image',cv2.WINDOW_NORMAL)
	while True:
		
		# Get capture
		capture = device.update()

		# Get the color image from the capture
		ret_color, color_image = capture.get_color_image()

		# Get the colored depth
		ret_depth, transformed_depth_image = capture.get_transformed_depth_image()

		if not ret_color or not ret_depth:
			continue

		pix_x = color_image.shape[1] // 2
		pix_y = color_image.shape[0] // 2
		rgb_depth = transformed_depth_image[pix_y, pix_x]

		pixels = k4a_float2_t((pix_x, pix_y))

		pos3d_color = device.calibration.convert_2d_to_3d(pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_COLOR)
		pos3d_depth = device.calibration.convert_2d_to_3d(pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH)
		print(f"RGB depth: {rgb_depth}, RGB pos3D: {pos3d_color}, Depth pos3D: {pos3d_depth}")

		# Overlay body segmentation on depth image
		cv2.imshow('Transformed Color Image',color_image)

		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):
			break