import _k4a
import traceback
import numpy as np
import cv2
import sys

class pyKinectAzure:

	def __init__(self,modulePath='C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'):

		self.k4a = _k4a.k4a(modulePath)

		self.device_handle = _k4a.k4a_device_t()
		self.capture_handle = _k4a.k4a_capture_t()	

	def device_get_installed_count(self):
		"""Gets the number of connected devices

		Parameters:
		None
			
		Returns:
		int: Number of sensors connected to the PC.
		
		Remarks:
		This API counts the number of Azure Kinect devices connected to the host PC.
		"""
		return int(self.k4a.k4a_device_get_installed_count())

	def device_open(self, index=0):
		"""Open an Azure Kinect device.

		Parameters:
		index (int): The index of the device to open, starting with
			
		Returns:
		None
		
		Remarks:
		If successful, k4a_device_open() will return a device handle in the device_handle parameter.
		This handle grants exclusive access to the device and may be used in the other Azure Kinect API calls.

		When done with the device, close the handle with k4a_device_close()
		"""
		self.VERIFY(self.k4a.k4a_device_open(index,self.device_handle),"Open K4A Device failed!")

	def device_close(self):
		"""Closes an Azure Kinect device.

		Parameters:
		None
			
		Returns:
		None
		
		Remarks:
		Once closed, the handle is no longer valid.

		Before closing the handle to the device, ensure that all captures have been released with
		k4a_capture_release().
		"""
		self.k4a.k4a_device_close(self.device_handle)

	def device_start_cameras(self, device_config=None):
		"""Starts color and depth camera capture.

		Parameters:
		device_config (k4a_device_configuration_t): The configuration we want to run the device in. This can be initialized with ::K4A_DEVICE_CONFIG_INIT_DEFAULT.
			
		Returns:
		None
		
		Remarks:
		Individual sensors configured to run will now start to stream captured data..

		It is not valid to call k4a_device_start_cameras() a second time on the same k4a_device_t until
		k4a_device_stop_cameras() has been called. 		
		"""
		if device_config is None:
			device_config = self.config()
			self.VERIFY(self.k4a.k4a_device_start_cameras(self.device_handle,device_config.current_config),"Start K4A cameras failed!")
			return

		self.VERIFY(self.k4a.k4a_device_start_cameras(self.device_handle,device_config.current_config),"Start K4A cameras failed!")


	def device_stop_cameras(self):
		"""Stops the color and depth camera capture..

		Parameters:
		None

		Returns:
		None
		
		Remarks:
		The streaming of individual sensors stops as a result of this call. Once called, k4a_device_start_cameras() may
		be called again to resume sensor streaming. 		
		"""

		self.k4a.k4a_device_stop_cameras(self.device_handle)


	def device_get_capture(self, timeout_in_ms=_k4a.K4A_WAIT_INFINITE):
		"""Reads a sensor capture.

		Parameters:h
		timeout_in_ms (int):Specifies the time in milliseconds the function should block waiting for the capture. If set to 0, the function will
							return without blocking. Passing a value of #K4A_WAIT_INFINITE will block indefinitely until data is available, the
							device is disconnected, or another error occurs.

		Returns:
		None

		Remarks:
		Gets the next capture in the streamed sequence of captures from the camera. If a new capture is not currently
		available, this function will block until the timeout is reached. The SDK will buffer at least two captures worth
		of data before dropping the oldest capture. Callers needing to capture all data need to ensure they read the data as
		fast as the data is being produced on average.

		Upon successfully reading a capture this function will return success and populate capture.
		If a capture is not available in the configured timeout_in_ms, then the API will return ::K4A_WAIT_RESULT_TIMEOUT.

		"""
		self.VERIFY(self.k4a.k4a_device_get_capture(self.device_handle,self.capture_handle,timeout_in_ms),"Get capture failed!")

	def capture_get_color_image(self):
		"""Get the color image associated with the given capture.

		Parameters:
		None
			
		Returns:
		k4a_image_t: Handle to the Image
		
		Remarks:
		Call this function to access the color image part of this capture. Release the ref k4a_image_t with
		k4a_image_release();
		"""

		return self.k4a.k4a_capture_get_color_image(self.capture_handle)

	def capture_get_depth_image(self):
		"""Get the depth image associated with the given capture.

		Parameters:
		None
			
		Returns:
		k4a_image_t: Handle to the Image
		
		Remarks:
		Call this function to access the depth image part of this capture. Release the \ref k4a_image_t with
		k4a_image_release();
		"""

		return self.k4a.k4a_capture_get_depth_image(self.capture_handle)

	def image_get_buffer(self, image_handle):
		"""Get the image buffer.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		ctypes.POINTER(ctypes.c_uint8): The function will return NULL if there is an error, and will normally return a pointer to the image buffer.
										Since all k4a_image_t instances are created with an image buffer, this function should only return NULL if the
										image_handle is invalid.

		Remarks:
		Use this buffer to access the raw image data.
		"""

		return self.k4a.k4a_image_get_buffer(image_handle)
		
	def image_get_size(self, image_handle):
		"""Get the image buffer size.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		int: The function will return 0 if there is an error, and will normally return the image size.
		Since all k4a_image_t instances are created with an image buffer, this function should only return 0 if the
		image_handle is invalid.

		Remarks:
		Use this function to know what the size of the image buffer is returned by k4a_image_get_buffer().
		"""

		return int(self.k4a.k4a_image_get_size(image_handle))

	def image_get_format(self, image_handle):
		"""Get the format of the image.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		int: This function is not expected to fail, all k4a_image_t's are created with a known format. If the
		image_handle is invalid, the function will return ::K4A_IMAGE_FORMAT_CUSTOM.

		Remarks:
		Use this function to determine the format of the image buffer.
		"""

		return int(self.k4a.k4a_image_get_format(image_handle))

	def image_get_width_pixels(self, image_handle):
		"""Get the image width in pixels.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		int: This function is not expected to fail, all k4a_image_t's are created with a known width. If the part
		image_handle is invalid, the function will return 0.
		"""

		return int(self.k4a.k4a_image_get_width_pixels(image_handle))

	def image_get_height_pixels(self, image_handle):
		"""Get the image height in pixels.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		int: This function is not expected to fail, all k4a_image_t's are created with a known height. If the part
		image_handle is invalid, the function will return 0.
		"""

		return int(self.k4a.k4a_image_get_height_pixels(image_handle))

	def image_convert_to_numpy(self, image_handle):
		"""Get the image data as a numpy array

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		numpy.ndarray: Numpy array with the image data
		"""

		# Get the pointer to the buffer containing the image data
		buffer_pointer = self.image_get_buffer(image_handle)

		# Get the size of the buffer
		image_size = self.image_get_size(image_handle)
		image_width = self.image_get_width_pixels(image_handle)
		image_height = self.image_get_height_pixels(image_handle)

		# Get the image format
		image_format = self.image_get_format(image_handle)
		# print(image_format)

		# Read the data in the buffer
		bufferArray = np.ctypeslib.as_array(buffer_pointer,shape=[image_size])

		# Parse buffer based on image format
		if image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_MJPG:
			return cv2.imdecode(np.frombuffer(bufferArray, dtype=np.uint8), -1)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_NV12:
			yuv_image = np.frombuffer(bufferArray, dtype=np.uint8).reshape(int(image_height*1.5),image_width)
			return cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_NV12)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_YUY2:
			yuv_image = np.frombuffer(bufferArray, dtype=np.uint8).reshape(image_height,image_width,2)
			return cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_YUY2)

	def image_release(self, image_handle):
		"""Remove a reference from the k4a_image_t.

		Parameters:
		image_handle (k4a_image_t): Handle to the Image

		Returns:
		None

		Remarks:
		References manage the lifetime of the object. When the references reach zero the object is destroyed. A caller must
		not access the object after its reference is released.
		"""

		self.k4a.k4a_image_release(image_handle)

	def capture_release(self):
		"""Release a capture.

		Parameters:
		None

		Returns:
		None

		Remarks:
		Call this function when finished using the capture.
		"""

		self.k4a.k4a_capture_release(self.capture_handle)

	class config:
		def __init__(self,
					color_format=_k4a.K4A_IMAGE_FORMAT_COLOR_MJPG,
					color_resolution=_k4a.K4A_COLOR_RESOLUTION_720P,
					depth_mode=_k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED,
					camera_fps=_k4a.K4A_FRAMES_PER_SECOND_30,
					synchronized_images_only=False,
					depth_delay_off_color_usec=0,
					wired_sync_mode=_k4a.K4A_WIRED_SYNC_MODE_STANDALONE,
					subordinate_delay_off_master_usec=0,
					disable_streaming_indicator=False):
			self.color_format = color_format
			self.color_resolution = color_resolution
			self.depth_mode = depth_mode
			self.camera_fps = camera_fps
			self.synchronized_images_only = synchronized_images_only
			self.depth_delay_off_color_usec = depth_delay_off_color_usec
			self.wired_sync_mode = wired_sync_mode
			self.subordinate_delay_off_master_usec = subordinate_delay_off_master_usec
			self.disable_streaming_indicator = disable_streaming_indicator

			self._on_change()

		def __setattr__(self, name, value):
			"""Run on change function when configuration parameters are changed
			"""
			if hasattr(self, name):
				if name != "current_config":
					if int(self.__dict__[name]) != value:
						self.__dict__[name] = value
						self._on_change()
				else:
					self.__dict__[name] = value
			else:
				self.__dict__[name] = value

		def __str__(self):
			"""Print the current settings and a short explanation"""
			message = (
				"Device configuration: \n"
				f"\tcolor_format: {self.color_format} (0:JPG, 1:NV12, 2:YUY2, 3:BGRA32)\n"
				f"\tcolor_resolution: {self.color_resolution} (0:OFF, 1:720p, 2:1080p, 3:1440p, 4:1536p, 5:2160p, 6:3072p)\n"
				f"\tdepth_mode: {self.depth_mode} (0:OFF, 1:NFOV_2X2BINNED, 2:NFOV_UNBINNED,3:WFOV_2X2BINNED, 4:WFOV_UNBINNED, 5:Passive IR)\n"
				f"\tcamera_fps: {self.camera_fps} (0:5 FPS, 1:15 FPS, 2:30 FPS)\n"
				f"\tsynchronized_images_only: {self.synchronized_images_only} (True of False). Drop images if the color and depth are not synchronized\n"
				f"\tdepth_delay_off_color_usec: {self.depth_delay_off_color_usec} ms. Delay between the color image and the depth image\n"
				f"\twired_sync_mode: {self.wired_sync_mode} (0:Standalone mode, 1:Master mode, 2:Subordinate mode)\n"
				f"\tsubordinate_delay_off_master_usec: {self.subordinate_delay_off_master_usec} ms. The external synchronization timing.\n"
				f"\tdisable_streaming_indicator: {self.disable_streaming_indicator} (True or False). Streaming indicator automatically turns on when the color or depth camera's are in use.\n"
				)
			return message

		def __repr__(self):
			"""Return the current configuration"""
			return self.current_config

		def _on_change(self):
			self.current_config =  _k4a.k4a_device_configuration_t(self.color_format, \
												self.color_resolution,\
												self.depth_mode,\
												self.camera_fps ,\
												self.synchronized_images_only,\
												self.depth_delay_off_color_usec,\
												self.wired_sync_mode,\
												self.subordinate_delay_off_master_usec,\
												self.disable_streaming_indicator)

	@staticmethod
	def VERIFY(result, error):
		if result != _k4a.K4A_RESULT_SUCCEEDED:
			print(error)
			traceback.print_stack()
			sys.exit(1)


	



