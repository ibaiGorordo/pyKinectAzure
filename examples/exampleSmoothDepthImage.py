import sys
import cv2
import numpy as np

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	cv2.namedWindow('Smoothed Depth Comparison',cv2.WINDOW_NORMAL)
	while True:
		
		# Get capture
		capture = device.update()

		# Get the color depth image from the capture
		ret, raw_depth_image = capture.get_colored_depth_image()

		if not ret:
			continue

		# Get the smooth depth image using Navier-Stokes based inpainting. maximum_hole_size defines 
		# the maximum hole size to be filled, bigger hole size will take longer time to process
		maximum_hole_size = 10
		ret, smooth_depth_color_image = capture.get_smooth_colored_depth_image(maximum_hole_size)
		
		# Concatenate images for comparison
		comparison_image = np.concatenate((raw_depth_image, smooth_depth_color_image), axis=1)
		comparison_image = cv2.putText(comparison_image, 'Original', (180, 50) , cv2.FONT_HERSHEY_SIMPLEX ,1.5, (255,255,255), 3, cv2.LINE_AA) 
		comparison_image = cv2.putText(comparison_image, 'Smoothed', (670, 50) , cv2.FONT_HERSHEY_SIMPLEX ,1.5, (255,255,255), 3, cv2.LINE_AA)

		# Plot the image
		cv2.imshow('Smoothed Depth Comparison',comparison_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break