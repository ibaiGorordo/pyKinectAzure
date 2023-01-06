import numpy as np
import cv2

from pykinect_azure.k4abt.joint2d import Joint2d
from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_COUNT, K4ABT_SEGMENT_PAIRS
from pykinect_azure.k4abt._k4abtTypes import k4abt_skeleton2D_t, k4abt_body2D_t, body_colors
from pykinect_azure.k4a._k4atypes import K4A_CALIBRATION_TYPE_DEPTH

class Body2d:
	def __init__(self, body2d_handle):

		if body2d_handle:
			self._handle = body2d_handle
			self.id = body2d_handle.id
			self.initialize_skeleton()

	def __del__(self):

		self.destroy()

	def json(self):
		return self._handle.__iter__()

	def numpy(self):
		return np.array([joint.numpy() for joint in self.joints])

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			self._handle = None

	def initialize_skeleton(self):
		joints = np.ndarray((K4ABT_JOINT_COUNT,),dtype=np.object_)

		for i in range(K4ABT_JOINT_COUNT):
			joints[i] = Joint2d(self._handle.skeleton.joints2D[i], i)

		self.joints = joints

	def draw(self, image, only_segments = False):

		color = (int (body_colors[self.id][0]), int (body_colors[self.id][1]), int (body_colors[self.id][2]))

		for segmentId in range(len(K4ABT_SEGMENT_PAIRS)):
			segment_pair = K4ABT_SEGMENT_PAIRS[segmentId]
			point1 = self.joints[segment_pair[0]].get_coordinates()
			point2 = self.joints[segment_pair[1]].get_coordinates()

			if (point1[0] == 0 and point1[1] == 0) or (point2[0] == 0 and point2[1] == 0):
				continue
			image = cv2.line(image, point1, point2,color, 2)

		if only_segments:
			return image

		for joint in self.joints:
			image = cv2.circle(image, joint.get_coordinates(), 3, color, 3)

		return image


	@staticmethod
	def create(body_handle, calibration, bodyIdx, dest_camera):

		skeleton2d_handle = k4abt_skeleton2D_t()
		body2d_handle = k4abt_body2D_t()

		for jointID,joint in enumerate(body_handle.skeleton.joints): 
			skeleton2d_handle.joints2D[jointID].position = calibration.convert_3d_to_2d(joint.position, K4A_CALIBRATION_TYPE_DEPTH, dest_camera)
			skeleton2d_handle.joints2D[jointID].confidence_level = joint.confidence_level

		body2d_handle.skeleton = skeleton2d_handle
		body2d_handle.id = bodyIdx

		return Body2d(body2d_handle)


	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = f"Body Id: {self.id}\n\n"

		for joint in self.joints:
			message += str(joint)

		return message

