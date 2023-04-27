import cv2

import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
	device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker()

	cv2.namedWindow('Color image with skeleton',cv2.WINDOW_NORMAL)
	cv2.namedWindow('Transformed Color image with skeleton',cv2.WINDOW_NORMAL)
	while True:
		
		# Get capture
		capture = device.update()

		# Get body tracker frame
		body_frame = bodyTracker.update()

		# Get the color image
		ret_color, color_image = capture.get_color_image()

		# Get the depth image
		ret_depth, depth_image = capture.get_depth_image()

		# Get the transformed color image
		ret_transformed_color, transformed_color_image = capture.get_transformed_color_image()

		# Get the point cloud
		ret_point, points = capture.get_pointcloud()

		# Get the transformed point cloud
		ret_transformed_point, transformed_points = capture.get_transformed_pointcloud()

		if not ret_color or not ret_depth or not ret_point or not ret_transformed_point or not ret_transformed_color:
			continue

		points_map = points.reshape((transformed_color_image.shape[0], transformed_color_image.shape[1], 3))
		transformed_points_map = transformed_points.reshape((color_image.shape[0], color_image.shape[1], 3))

		for body_id in range(body_frame.get_num_bodies()):
			color_skeleton_2d = body_frame.get_body2d(body_id, pykinect.K4A_CALIBRATION_TYPE_COLOR).numpy()
			depth_skeleton_2d = body_frame.get_body2d(body_id, pykinect.K4A_CALIBRATION_TYPE_DEPTH).numpy()
			skeleton_3d = body_frame.get_body(body_id).numpy()

			color_neck_2d = color_skeleton_2d[pykinect.K4ABT_JOINT_NECK,:]
			depth_neck_2d = depth_skeleton_2d[pykinect.K4ABT_JOINT_NECK,:]

			depth_neck_float2 = pykinect.k4a_float2_t(depth_neck_2d)
			depth = depth_image[int(depth_neck_2d[1]), int(depth_neck_2d[0])]
			depth_neck_float3 = device.calibration.convert_2d_to_3d(depth_neck_float2, depth, pykinect.K4A_CALIBRATION_TYPE_DEPTH, pykinect.K4A_CALIBRATION_TYPE_DEPTH)
			depth_transformed_neck_3d = [depth_neck_float3.xyz.x, depth_neck_float3.xyz.y, depth_neck_float3.xyz.z]

			color_neck_3d = transformed_points_map[int(color_neck_2d[1]), int(color_neck_2d[0]), :]
			depth_neck_3d = points_map[int(depth_neck_2d[1]), int(depth_neck_2d[0]), :]
			neck_3d = skeleton_3d[pykinect.K4ABT_JOINT_NECK,:3]
			print(f'Neck 3D coordinates: color = {color_neck_3d}, depth = {depth_neck_3d}, depth converted = {depth_transformed_neck_3d}, body = {neck_3d}')


		# Draw the skeletons into the color image
		color_skeleton = body_frame.draw_bodies(color_image, pykinect.K4A_CALIBRATION_TYPE_COLOR)
		transformed_color_skeleton = body_frame.draw_bodies(transformed_color_image, pykinect.K4A_CALIBRATION_TYPE_DEPTH)

		# Overlay body segmentation on depth image
		cv2.imshow('Color image with skeleton', color_skeleton)
		cv2.imshow('Transformed Color image with skeleton', transformed_color_skeleton)

		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):
			break

