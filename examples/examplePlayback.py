import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

	video_filename = "output.mkv"

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Start playback
	playback = pykinect.start_playback(video_filename)

	playback_config = playback.get_record_configuration()
	# print(playback_config)

	cv2.namedWindow('Depth Image',cv2.WINDOW_NORMAL)
	while playback.isOpened():

		# Get camera capture
		capture = playback.update()

		# Get the colored depth
		ret, depth_color_image = capture.get_colored_depth_image()
		
		# Plot the image
		cv2.imshow('Depth Image',depth_color_image)
		
		# Press q key to stop
		if cv2.waitKey(30) == ord('q'): 
			break