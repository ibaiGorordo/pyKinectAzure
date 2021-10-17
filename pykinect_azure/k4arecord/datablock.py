from pykinect_azure.k4arecord import _k4arecord
from pykinect_azure.k4a import _k4a

class Datablock:

	def __init__(self, modulePath):
		self._handle = _k4arecord.k4a_playback_data_block_t()

	def __del__(self):
		self.reset()

	def is_valid(self):
		return self.datablock_handle != None

	def handle(self):
		return self._handle

	def reset(self):
		if self.is_valid():
			_k4arecord.k4a_playback_data_block_release(self._handle)
			self._handle = None

	def get_device_timestamp_usec(self):
		return int(_k4arecord.k4a_playback_data_block_get_device_timestamp_usec(self._handle))

	def get_buffer_size(self):
		return int(_k4arecord.k4a_playback_data_block_get_buffer_size(self._handle))

	def get_buffer(self):
		if not self.is_valid():
			return None
			
		return _k4arecord.k4a_playback_data_block_get_buffer(self._handle)