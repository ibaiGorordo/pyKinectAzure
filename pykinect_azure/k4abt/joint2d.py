import numpy as np
from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_NAMES

class Joint2d:

	def __init__(self, joint2d_handle, id):

		if joint2d_handle:
			self._handle = joint2d_handle
			self.position = joint2d_handle.position.xy
			self.confidence_level = joint2d_handle.confidence_level
			self.id = id
			self.name = self.get_name()

	def __del__(self):

		self.destroy()

	def numpy(self):
		return np.array([self.position.x,self.position.y])

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			self._handle = None

	def get_coordinates(self):
		return (int(self.position.x), int(self.position.y))

	def get_name(self):
		return K4ABT_JOINT_NAMES[self.id]

	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = (
			f"{self.name} Joint 2d info: \n"
			f"\tPixel: [{self.position.x},{self.position.y}]\n"
			f"\tconfidence: {self.confidence_level} \n\n")
		return message
