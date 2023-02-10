import numpy as np
import cv2 

from pykinect_azure.k4abt import _k4abt
from pykinect_azure.k4abt.body import Body
from pykinect_azure.k4abt.body2d import Body2d
from pykinect_azure.k4abt._k4abtTypes import k4abt_body_t, body_colors
from pykinect_azure.k4a import Image, Capture, Transformation
from pykinect_azure.k4a._k4atypes import K4A_CALIBRATION_TYPE_DEPTH

class Frame:
	def __init__(self, frame_handle, calibration):

		if frame_handle:
			self._handle = frame_handle
			self.calibration = calibration
			self.transformation = Transformation(self.calibration)
			_k4abt.k4abt_frame_reference(self._handle)

	def __del__(self):
		self.reset()

	def json(self):

		bodies = self.get_bodies()

		if not bodies:
			return ""

		return [body.json() for body in bodies]

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def reset(self):
		if self.is_valid():
			self.release()
			self._handle = None

	def release(self):
		if self.is_valid():
			_k4abt.k4abt_frame_release(self._handle)

	def get_num_bodies(self):
		return _k4abt.k4abt_frame_get_num_bodies(self._handle)

	def get_body_skeleton(self, index=0):
		skeleton = _k4abt.k4abt_skeleton_t()

		_k4abt.VERIFY(_k4abt.k4abt_frame_get_body_skeleton(self._handle, index, skeleton), "Body tracker get body skeleton failed!")

		return skeleton

	def get_body_id(self, index=0):
		return _k4abt.k4abt_frame_get_body_id(self._handle, index)

	def get_bodies(self):

		bodies = []

		# Get the number of people in the frame
		num_bodies = self.get_num_bodies()

		# Extract the skeleton of each person
		if num_bodies:
			for bodyIdx in range(num_bodies):
				bodies.append(self.get_body(bodyIdx))

		return bodies

	def get_body(self, bodyIdx = 0):
		body_handle = k4abt_body_t()
		body_handle.id = self.get_body_id(bodyIdx);
		body_handle.skeleton = self.get_body_skeleton(bodyIdx);

		return Body(body_handle)

	def get_body2d(self, bodyIdx = 0, dest_camera = K4A_CALIBRATION_TYPE_DEPTH):

		body_handle = self.get_body(bodyIdx).handle()

		return Body2d.create(body_handle, self.calibration, bodyIdx, dest_camera)

	def draw_bodies(self, destination_image, dest_camera = K4A_CALIBRATION_TYPE_DEPTH, only_segments = False):
		num_bodies = self.get_num_bodies()

		for body_id in range(num_bodies):
			destination_image = self.draw_body2d(destination_image, body_id, dest_camera, only_segments)

		return destination_image

	def draw_body2d(self, destination_image, bodyIdx = 0, dest_camera = K4A_CALIBRATION_TYPE_DEPTH, only_segments = False):
		return self.get_body2d(bodyIdx, dest_camera).draw(destination_image, only_segments)

	def get_device_timestamp_usec(self):
		return _k4abt.k4abt_frame_get_device_timestamp_usec(self._handle)

	def get_body_index_map(self):
		return Image(_k4abt.k4abt_frame_get_body_index_map(self._handle))

	def get_body_index_map_image(self):
		return self.get_body_index_map().to_numpy()

	def get_transformed_body_index_map(self):
		depth_image = self.get_capture().get_depth_image_object()	
		return self.transformation.depth_image_to_color_camera_custom(depth_image, self.get_body_index_map())

	def get_transformed_body_index_map_image(self):
		transformed_body_index_map =self.get_transformed_body_index_map()
		return transformed_body_index_map.to_numpy()

	def get_segmentation_image(self):
		ret, body_index_map = self.get_body_index_map_image()
		return ret, np.dstack([cv2.LUT(body_index_map, body_colors[:,i]) for i in range(3)])

	def get_transformed_segmentation_image(self):
		ret, transformed_body_index_map = self.get_transformed_body_index_map_image()
		return ret, np.dstack([cv2.LUT(transformed_body_index_map, body_colors[:,i]) for i in range(3)])
		
	def get_capture(self):
		return Capture(_k4abt.k4abt_frame_get_capture(self._handle), self.calibration._handle)

