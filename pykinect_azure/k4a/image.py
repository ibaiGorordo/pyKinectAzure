import numpy as np
import cv2

from pykinect_azure.k4a import _k4a

class Image:
	_handle = None
	buffer_pointer = None

	def __init__(self, image_handle=None):

		self._handle = image_handle
		# Get the pointer to the buffer containing the image data
		self.buffer_pointer = self.get_buffer() if self.is_valid() else None

	def __del__(self):

		self.reset()

	def is_valid(self):
		return self._handle or self.buffer_pointer is not None

	def handle(self):
		return self._handle

	def reset(self):
		if self.is_valid():
			_k4a.k4a_image_release(self._handle)
			self._handle = None

	@staticmethod
	def create(image_format,width_pixels,height_pixels,stride_bytes):
		handle = _k4a.k4a_image_t()
		_k4a.VERIFY(_k4a.k4a_image_create(image_format,width_pixels,height_pixels,stride_bytes,handle),"Create image failed!")

		return Image(handle)

	@property
	def width(self):
		return self.get_width_pixels()
		
	@property
	def height(self):
		return self.get_height_pixels()

	@property
	def stride(self):
		return self.get_stride_bytes()

	@property
	def format(self):
		return self.get_format()

	@property
	def size(self):
		return self.get_size()


	def get_buffer(self):
		if not self._handle:
			return None

		return _k4a.k4a_image_get_buffer(self._handle)
		
	def get_size(self):
		if not self.is_valid():
			return None

		return int(_k4a.k4a_image_get_size(self._handle))

	def get_format(self):
		if not self.is_valid():
			return None

		return int(_k4a.k4a_image_get_format(self._handle))

	def get_width_pixels(self):
		if not self.is_valid():
			return None

		return int(_k4a.k4a_image_get_width_pixels(self._handle))

	def get_height_pixels(self):
		if not self.is_valid():
			return None

		return int(_k4a.k4a_image_get_height_pixels(self._handle))

	def get_stride_bytes(self):
		return int(_k4a.k4a_image_get_stride_bytes(self._handle))

	def to_numpy(self):

		if not self.is_valid():
			return False, None

		# Get the size of the buffer
		image_size = self.get_size()
		image_width = self.get_width_pixels()
		image_height = self.get_height_pixels()

		# Get the image format
		image_format = self.get_format()

		# Read the data in the buffer
		buffer_array = np.ctypeslib.as_array(self.buffer_pointer,shape=(image_size,))

		# Parse buffer based on image formats
		if image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_MJPG:
			return True, cv2.imdecode(np.frombuffer(buffer_array, dtype=np.uint8).copy(), -1)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_NV12:
			yuv_image = np.frombuffer(buffer_array, dtype=np.uint8).copy().reshape(int(image_height*1.5),image_width)
			return True, cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_NV12)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_YUY2:
			yuv_image = np.frombuffer(buffer_array, dtype=np.uint8).copy().reshape(image_height,image_width,2)
			return True, cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_YUY2)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32:
			return True, np.frombuffer(buffer_array, dtype=np.uint8).copy().reshape(image_height,image_width,4)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_DEPTH16:
			return True, np.frombuffer(buffer_array, dtype="<u2").copy().reshape(image_height,image_width)#little-endian 16 bits unsigned Depth data
		elif image_format == _k4a.K4A_IMAGE_FORMAT_IR16:
			return True, np.frombuffer(buffer_array, dtype="<u2").copy().reshape(image_height,image_width)#little-endian 16 bits unsigned IR data. For more details see: https://microsoft.github.io/Azure-Kinect-Sensor-SDK/release/1.2.x/namespace_microsoft_1_1_azure_1_1_kinect_1_1_sensor_a7a3cb7a0a3073650bf17c2fef2bfbd1b.html
		elif image_format == _k4a.K4A_IMAGE_FORMAT_CUSTOM8:
			return True, np.frombuffer(buffer_array, dtype="<u1").copy().reshape(image_height,image_width)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_CUSTOM16:
			return True, np.frombuffer(buffer_array, dtype="<u2").copy().reshape(image_height,image_width)
		elif image_format == _k4a.K4A_IMAGE_FORMAT_CUSTOM:
			return True, np.frombuffer(buffer_array, dtype="<i2").copy()