from _k4a import k4a
import _k4atypes as k4atypes
import traceback

class pyKinectAzure:

	def __init__(self,modulePath='C:\\Program Files\\Azure Kinect SDK v1.4.0\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'):

		self.k4a = k4a(modulePath)

		self.device_handle = k4atypes.k4a_device_t()
		self.capture_handle = k4atypes.k4a_capture_t()	

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

	def device_start_cameras(self, device_config=k4atypes.K4A_DEVICE_CONFIG_INIT_DEFAULT):
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

		self.VERIFY(self.k4a.k4a_device_start_cameras(self.device_handle,device_config),"Start K4A cameras failed!")


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


	def device_get_capture(self, timeout_in_ms=k4atypes.K4A_WAIT_INFINITE):
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

	@staticmethod
	def VERIFY(result, error):
		if result != k4atypes.K4A_RESULT_SUCCEEDED:
			print(error)
			traceback.print_stack()
			sys.exit(1)


	



