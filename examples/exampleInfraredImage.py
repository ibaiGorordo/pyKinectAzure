import cv2

import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	cv2.namedWindow('Infrared Image',cv2.WINDOW_NORMAL)
	while True:

		# Get capture
		capture = device.update()

		# Get the infrared image
		ret, ir_image = capture.get_ir_image()

		if not ret:
			continue
	
		# Plot image
		cv2.imshow('Infrared Image',ir_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break