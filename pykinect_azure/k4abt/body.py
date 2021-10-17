import numpy as np

from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_COUNT
from pykinect_azure.k4abt.joint import Joint

class Body:
	def __init__(self, skeleton_handle):

		if skeleton_handle:
			self._handle = skeleton_handle
			self.initialize()

	def __del__(self):
		self.destroy()

	def is_valid(self):
		return self._handle

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			self._handle = None

	def initialize(self):
		joints = np.ndarray((K4ABT_JOINT_COUNT,),dtype=np.object)

		for i in range(K4ABT_JOINT_COUNT):
			joints[i] = Joint(self._handle.skeleton.joints[i], i)
			
		self.joints = joints

	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = (
			"Joint info: \n"
			f"\tposition: [{self.position.x},{self.position.y},{self.position.z}]\n"
			f"\torientation: [{self.orientation.w},{self.orientation.x},{self.orientation.y},{self.orientation.z}]\n"
			f"\tconfidence: {self.tconfidence} \n")
		return message


