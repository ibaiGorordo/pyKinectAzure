import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

	video_filename = "output.mkv"

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)

	# Start playback
	playback = pykinect.start_playback(video_filename)

	playback_config = playback.get_record_configuration()
	# print(playback_config)

	playback_calibration = playback.get_calibration()

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker(calibration=playback_calibration)

	cv2.namedWindow('Depth image with skeleton',cv2.WINDOW_NORMAL)
	while playback.isOpened():

		# Get camera capture
		capture = playback.update()

		# Get body tracker frame
		body_frame = bodyTracker.update(capture=capture)

		# Get the colored depth
		ret, depth_color_image = capture.get_colored_depth_image()

		# Get the colored body segmentation
		ret, body_image_color = body_frame.get_segmentation_image()
		
		if not ret:
			continue
			
		# Combine both images
		combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

		# Draw the skeletons
		combined_image = body_frame.draw_bodies(combined_image)

		# Overlay body segmentation on depth image
		cv2.imshow('Depth image with skeleton',combined_image)

		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):  
			break