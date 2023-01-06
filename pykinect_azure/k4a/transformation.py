import ctypes

from pykinect_azure.k4a import _k4a
from pykinect_azure.k4a.image import Image

class Transformation:

	def __init__(self, calibration_handle):
		self._handle = _k4a.k4a_transformation_create(calibration_handle)
		self.color_resolution = Resolution(calibration_handle.color_camera_calibration.resolution_width, calibration_handle.color_camera_calibration.resolution_height)
		self.depth_resolution = Resolution(calibration_handle.depth_camera_calibration.resolution_width, calibration_handle.depth_camera_calibration.resolution_height)	

	def __del__(self):
		self.destroy()

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			_k4a.k4a_transformation_destroy(self._handle)
			self._handle = None

	def depth_image_to_color_camera(self, depth_image):

		if not depth_image.is_valid():
			return Image()

		transformed_depth_image = Image.create(depth_image.format,
												self.color_resolution.width,
												self.color_resolution.height,
												self.color_resolution.width*2)

		_k4a.k4a_transformation_depth_image_to_color_camera(self._handle, depth_image.handle(), transformed_depth_image.handle())

		return transformed_depth_image

	def depth_image_to_color_camera_custom(self, depth_image, custom_image, interpolation = _k4a.K4A_TRANSFORMATION_INTERPOLATION_TYPE_LINEAR):
		
		if not depth_image.is_valid() or not custom_image.is_valid():
			return Image()

		transformed_custom_image = Image.create(custom_image.format,
												self.color_resolution.width,
												self.color_resolution.height,
												self.color_resolution.width*self.get_custom_bytes_per_pixel(custom_image))

		transformed_depth_image = Image.create(_k4a.K4A_IMAGE_FORMAT_DEPTH16,
												self.color_resolution.width,
												self.color_resolution.height,
												self.color_resolution.width*2)

		invalid_custom_value = ctypes.c_uint32()

		_k4a.k4a_transformation_depth_image_to_color_camera_custom(self._handle, depth_image.handle(), custom_image.handle(), transformed_depth_image.handle(), transformed_custom_image.handle(), interpolation, invalid_custom_value)

		return transformed_custom_image



	def color_image_to_depth_camera(self, depth_image, color_image):

		if not depth_image.is_valid() or not color_image.is_valid():
			return Image()

		transformed_color_image = Image.create(_k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32,
												self.depth_resolution.width,
												self.depth_resolution.height,
												self.depth_resolution.width*4)

		_k4a.k4a_transformation_color_image_to_depth_camera(self._handle, depth_image.handle(), color_image.handle(), transformed_color_image.handle())

		return transformed_color_image

	def depth_image_to_point_cloud(self, depth_image, calibration_type = _k4a.K4A_CALIBRATION_TYPE_DEPTH):

		if not depth_image.is_valid():
			return Image()

		xyz_image = Image.create(_k4a.K4A_IMAGE_FORMAT_CUSTOM,
									depth_image.get_width_pixels(), 
									depth_image.get_height_pixels(),
									depth_image.get_width_pixels()*3*2)

		_k4a.k4a_transformation_depth_image_to_point_cloud(self._handle, depth_image.handle(), calibration_type, xyz_image.handle())

		return xyz_image

	def get_custom_bytes_per_pixel(self, custom_image):
		custom_image_format = custom_image.format

		if custom_image_format == _k4a.K4A_IMAGE_FORMAT_CUSTOM8:
			return 1
		else:
			return 2

class Resolution:

		def __init__(self, width, height):
			self.width = width
			self.height = height