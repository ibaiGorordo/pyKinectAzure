import cv2 

from pykinect_azure.k4a import _k4a
from pykinect_azure.k4a.image import Image
from pykinect_azure.k4a.transformation import Transformation
from pykinect_azure.utils.postProcessing import smooth_depth_image

class Capture:

	def __init__(self, capture_handle, calibration_handle):

		self._handle = capture_handle
		self.calibration_handle = calibration_handle
		self.camera_transform = Transformation(calibration_handle)

	def __del__(self):
		self.reset()

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def reset(self):
		if self.is_valid():
			self.release_handle()
			self._handle = None

	def release_handle(self):
		if self.is_valid():
			_k4a.k4a_capture_release(self._handle)

	@staticmethod
	def create():

		handle = _k4a.k4a_capture_t
		_k4a.VERIFY(Capture._k4a.k4a_capture_create(handle),"Create capture failed!")

		return Capture(handle)

	def get_color_image_object(self):
		
		return Image(_k4a.k4a_capture_get_color_image(self._handle))

	def get_depth_image_object(self):

		return Image(_k4a.k4a_capture_get_depth_image(self._handle))

	def get_ir_image_object(self):

		return Image(_k4a.k4a_capture_get_ir_image(self._handle))

	def get_transformed_depth_object(self):
		return self.camera_transform.depth_image_to_color_camera(self.get_depth_image_object())

	def get_transformed_color_object(self):
		return self.camera_transform.color_image_to_depth_camera(self.get_depth_image_object(),self.get_color_image_object())

	def get_pointcloud_object(self, calibration_type = _k4a.K4A_CALIBRATION_TYPE_DEPTH):
		return self.camera_transform.depth_image_to_point_cloud(self.get_depth_image_object(), calibration_type)

	def get_color_image(self):
		return self.get_color_image_object().to_numpy()

	def get_depth_image(self):

		return self.get_depth_image_object().to_numpy()

	def get_colored_depth_image(self):
		ret, depth_image = self.get_depth_image()
		if not ret:
			return ret, None

		return ret, self.color_depth_image(depth_image)

	def get_ir_image(self):
		return self.get_ir_image_object().to_numpy()

	def get_transformed_depth_image(self):
		return self.get_transformed_depth_object().to_numpy()

	def get_transformed_colored_depth_image(self):
		ret, transformed_depth_image = self.get_transformed_depth_image()

		return ret, self.color_depth_image(transformed_depth_image)

	def get_transformed_color_image(self):
		return self.get_transformed_color_object().to_numpy()

	def get_smooth_depth_image(self, maximum_hole_size=10):
		ret, depth_image = self.get_depth_image()
		return ret, smooth_depth_image(depth_image,maximum_hole_size)

	def get_smooth_colored_depth_image(self, maximum_hole_size=10):
		ret, smooth_depth_image = self.get_smooth_depth_image(maximum_hole_size)
		return ret, self.color_depth_image(smooth_depth_image)

	def get_pointcloud(self, calibration_type = _k4a.K4A_CALIBRATION_TYPE_DEPTH):
		ret, points = self.get_pointcloud_object(calibration_type).to_numpy()
		points = points.reshape((-1, 3))
		return ret, points

	@staticmethod
	def color_depth_image(depth_image):
		depth_color_image = cv2.convertScaleAbs (depth_image, alpha=0.05)  #alpha is fitted by visual comparison with Azure k4aviewer results 
		depth_color_image = cv2.applyColorMap(depth_color_image, cv2.COLORMAP_JET)

		return depth_color_image







