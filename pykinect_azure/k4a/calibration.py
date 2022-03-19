import ctypes

from pykinect_azure.k4a import _k4a

class Calibration:

	def __init__(self, calibration_handle):

		self._handle = calibration_handle

	def __del__(self):

		self.reset()
		
	def __str__(self):
		params = self._handle.color_camera_calibration.intrinsics.parameters.param
		message = (
			"Rgb Intrinsic parameters: \n"
			f"\tcx: {params.cx}\n"
			f"\tcy: {params.cy}\n"
			f"\tfx: {params.fx}\n"
			f"\tfy: {params.fy}\n"
			f"\tk1: {params.k1}\n"
			f"\tk2: {params.k2}\n"
			f"\tk3: {params.k3}\n"
			f"\tk4: {params.k4}\n"
			f"\tk5: {params.k5}\n"
			f"\tk6: {params.k6}\n"
			f"\tcodx: {params.codx}\n"
			f"\tcody: {params.cody}\n"
			f"\tp2: {params.p2}\n"
			f"\tp1: {params.p1}\n"
			f"\tmetric_radius: {params.metric_radius}\n"
			)
		return message

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def reset(self):
		if self.is_valid():
			self._handle = None

	def convert_3d_to_3d(self, source_point3d, source_camera, target_camera):
		target_point3d = _k4a.k4a_float3_t()

		_k4a.VERIFY(_k4a.k4a_calibration_3d_to_3d(self._handle, source_point3d,source_camera,target_camera,target_point3d),"Failed to convert from 3D to 3D")

		return target_point3d

	def convert_2d_to_3d(self, source_point2d, source_depth, source_camera, target_camera):
		target_point3d = _k4a.k4a_float3_t()
		valid = ctypes.c_int()

		_k4a.VERIFY(_k4a.k4a_calibration_2d_to_3d(self._handle, source_point2d, source_depth, source_camera,target_camera,target_point3d, valid),"Failed to convert from 2D to 3D")

		return target_point3d

	def convert_3d_to_2d(self, source_point3d, source_camera, target_camera):
		target_point2d = _k4a.k4a_float2_t()
		valid = ctypes.c_int()

		_k4a.VERIFY(_k4a.k4a_calibration_3d_to_2d(self._handle, source_point3d, source_camera,target_camera,target_point2d, valid),"Failed to convert from 3D to 2D")

		return target_point2d

	def convert_2d_to_2d(self, source_point2d, source_depth, source_camera, target_camera):
		target_point2d = _k4a.k4a_float2_t()
		valid = ctypes.c_int()

		_k4a.VERIFY(_k4a.k4a_calibration_2d_to_2d(self._handle, source_point2d, source_depth, source_camera,target_camera,target_point2d, valid),"Failed to convert from 2D to 2D")

		return target_point2d

	def convert_color_2d_to_depth_2d(self, source_point2d, depth_image):
		target_point2d = _k4a.k4a_float2_t()
		valid = ctypes.c_int()

		_k4a.VERIFY(_k4a.k4a._k4a_calibration_color_2d_to_depth_2d(self._handle, source_point2d, depth_image, target_point2d, valid),"Failed to convert from Color 2D to Depth 2D")

		return target_point2d








