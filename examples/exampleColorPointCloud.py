import cv2

import pykinect_azure as pykinect
from utils import Open3dVisualizer

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED
	# print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	# Initialize the Open3d visualizer
	open3dVisualizer = Open3dVisualizer()

	cv2.namedWindow('Transformed color',cv2.WINDOW_NORMAL)
	while True:

		# Get capture
		capture = device.update()

		# Get the 3D point cloud
		ret_point, points = capture.get_transformed_pointcloud()

		# Get the color image in the depth camera axis
		ret_color, color_image = capture.get_color_image()

		if not ret_color or not ret_point:
			continue

		open3dVisualizer(points, color_image)

		cv2.imshow('Transformed color', color_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break