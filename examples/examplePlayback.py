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

    cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
    while True:

        # Get camera capture
        ret, capture = playback.update()

        if not ret:
            break

        # Get color image
        ret_color, depth_color_image = capture.get_color_image()

        # Get the colored depth
        ret_depth, depth_color_image = capture.get_color_image()

        if not ret_color or not ret_depth:
            continue

        # Plot the image
        cv2.imshow('Depth Image', depth_color_image)

        # Press q key to stop
        if cv2.waitKey(30) == ord('q'):
            break
