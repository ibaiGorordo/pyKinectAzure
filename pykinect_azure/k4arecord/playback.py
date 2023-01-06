from pykinect_azure.k4arecord import _k4arecord
from pykinect_azure.k4arecord.datablock import Datablock
from pykinect_azure.k4arecord.record_configuration import RecordConfiguration

from pykinect_azure.k4a import _k4a
from pykinect_azure.k4a.capture import Capture
from pykinect_azure.k4a.calibration import Calibration
from pykinect_azure.k4a.imu_sample import ImuSample

class Playback:

	def __init__(self, filepath):
		
		self._handle = _k4arecord.k4a_playback_t()
		self._capture = None
		self._datablock = None

		self.open(filepath)
		self.calibration = self.get_calibration()	

	def __del__(self):
		self.close()

	def open(self, filepath):

		_k4arecord.VERIFY(_k4arecord.k4a_playback_open(filepath.encode('utf-8'),self._handle),"Failed to open recording!")

	def update(self):
		return self.get_next_capture()

	def is_valid(self):
		return self._handle != None

	def is_capture_initialized(self):
		return self._capture

	def is_datablock_initialized(self):
		return self._datablock

	def close(self):
		if self.is_valid():
			_k4arecord.k4a_playback_close(self._handle)
			self._handle = None			

	def get_calibration(self):
		calibration_handle = _k4arecord.k4a_calibration_t()
		if self.is_valid():		
			_k4arecord.VERIFY(_k4arecord.k4a_playback_get_calibration(self._handle, calibration_handle),"Failed to read device calibration from recording!")

		return Calibration(calibration_handle)

	def get_record_configuration(self):
		config = _k4arecord.k4a_record_configuration_t()

		if self.is_valid():		
			_k4arecord.VERIFY(_k4arecord.k4a_playback_get_record_configuration(self._handle, config),"Failed to read record configuration!")

		return RecordConfiguration(config)

	def get_next_capture(self):
		capture_handle = _k4a.k4a_capture_t()

		if self.is_capture_initialized():
			self._capture.release_handle()
			self._capture._handle = capture_handle
		else:
			self._capture = Capture(capture_handle, self.calibration.handle())

		ret = _k4arecord.k4a_playback_get_next_capture(self._handle, capture_handle) != _k4arecord.K4A_STREAM_RESULT_EOF


		return ret, self._capture

	def get_previous_capture(self):
		capture_handle = _k4a.k4a_capture_t()

		if self.is_capture_initialized():
			self._capture.release_handle()
			self._capture._handle = capture_handle
		else:
			self._capture = Capture(capture_handle, self.calibration.handle())

		ret = _k4arecord.k4a_playback_get_previous_capture(self._handle, capture_handle) != _k4arecord.K4A_STREAM_RESULT_EOF

		return ret, self._capture

	def get_next_imu_sample(self):
		imu_sample_struct = _k4a.k4a_imu_sample_t()
		_k4a.VERIFY(_k4arecord.k4a_playback_get_next_imu_sample(self._handle, imu_sample_struct),"Get next imu sample failed!")
			
		# Convert the structure into a dictionary
		_imu_sample = ImuSample(imu_sample_struct)

		return _imu_sample

	def get_previous_imu_sample(self):
		imu_sample_struct = _k4a.k4a_imu_sample_t()
		_k4a.VERIFY(_k4arecord.k4a_playback_get_previous_imu_sample(self._handle, imu_sample_struct),"Get previous imu sample failed!")
			
		# Convert the structure into a dictionary
		_imu_sample = ImuSample(imu_sample_struct)

		return _imu_sample

	def seek_timestamp(self, offset = 0, origin = _k4arecord.K4A_PLAYBACK_SEEK_BEGIN):
		_k4a.VERIFY(_k4arecord.k4a_playback_seek_timestamp(self._handle, offset, origin),"Seek recording failed!")
			
	def get_recording_length(self):
		return int(_k4arecord.k4a_playback_get_recording_length_usec(self._handle))

	def set_color_conversion(self, format = _k4a.K4A_IMAGE_FORMAT_DEPTH16):
		_k4a.VERIFY(_k4arecord.k4a_playback_set_color_conversion(self._handle, format),"Seek color conversio failed!")

	def get_next_data_block(self, track):
		block_handle = _k4arecord.k4a_playback_data_block_t()
		_k4a.VERIFY(_k4arecord.k4a_playback_get_next_data_block(self._handle, track, block_handle),"Get next data block failed!")
			
		if self.is_datablock_initialized():
			self._datablock._handle = block_handle
		else :
			self._datablock = Datablock(block_handle)

		return self._datablock

	def get_previous_data_block(self, track):
		block_handle = _k4arecord.k4a_playback_data_block_t()
		_k4a.VERIFY(_k4arecord.k4a_playback_get_previous_data_block(self._handle, track, block_handle),"Get previous data block failed!")
			
		if self.is_datablock_initialized():
			self._datablock._handle = block_handle
		else :
			self._datablock = Datablock(block_handle)

		return self._datablock
