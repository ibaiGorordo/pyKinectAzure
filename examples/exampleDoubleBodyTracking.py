import sys
import cv2

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    # Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
    # print(device_config)

    # Start device
    device = pykinect.start_device(config=device_config, device_index=0)
    device1 = pykinect.start_device(config=device_config, device_index=1)

    # Start body tracker
    bodyTracker = pykinect.start_body_tracker()
    bodyTracker1 = pykinect.start_body_tracker()

    cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Depth image with skeleton1', cv2.WINDOW_NORMAL)
    while True:

        # Get capture
        capture = device.update()
        capture1 = device1.update()

        # Get body tracker frame
        body_frame = bodyTracker.update(capture)
        body_frame1 = bodyTracker1.update(capture1)

        # Get the color depth image from the capture
        ret, depth_color_image = capture.get_colored_depth_image()
        ret, depth_color_image1 = capture1.get_colored_depth_image()

        # Get the colored body segmentation
        ret, body_image_color = body_frame.get_segmentation_image()
        ret, body_image_color1 = body_frame1.get_segmentation_image()
        if not ret:
            continue

        # Combine both images
        combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)
        combined_image1 = cv2.addWeighted(depth_color_image1, 0.6, body_image_color1, 0.4, 0)

        # Draw the skeletons
        combined_image = body_frame.draw_bodies(combined_image)
        combined_image1 = body_frame1.draw_bodies(combined_image1)

        # Overlay body segmentation on depth image
        cv2.imshow('Depth image with skeleton', combined_image)
        cv2.imshow('Depth image with skeleton1', combined_image1)

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
