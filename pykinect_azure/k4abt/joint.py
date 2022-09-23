import numpy as np
from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_NAMES

class Joint:
	def __init__(self, joint_handle, id):

		if joint_handle:
			self._handle = joint_handle
			self.position = joint_handle.position.xyz
			self.orientation = joint_handle.orientation.wxyz
			self.confidence_level = joint_handle.confidence_level
			self.id = id
			self.name = self.get_name()

	def __del__(self):

		self.destroy()

	def numpy(self):
		return np.array([self.position.x, self.position.y, self.position.z,
						 self.orientation.w, self.orientation.x, self.orientation.y, self.orientation.z,
						 self.confidence_level])

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			self._handle = None

	def get_name(self):
		return K4ABT_JOINT_NAMES[self.id]

	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = (
			f"{self.name} Joint info: \n"
			f"\tposition: [{self.position.x},{self.position.y},{self.position.z}]\n"
			f"\torientation: [{self.orientation.w},{self.orientation.x},{self.orientation.y},{self.orientation.z}]\n"
			f"\tconfidence: {self.confidence_level} \n\n")
		return message
