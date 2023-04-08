from pykinect_azure.k4abt import _k4abt
from pykinect_azure.k4abt.frame import Frame
from pykinect_azure.k4abt._k4abtTypes import k4abt_tracker_default_configuration
from pykinect_azure.k4a.device import Device
from pykinect_azure.k4a._k4atypes import K4A_WAIT_INFINITE
from pykinect_azure.utils import get_k4abt_lite_model_path

class Tracker:
	_handle = None
	def __init__(self, calibration, model_type):

		self.calibration = calibration
		self._handle = self.create(model_type)
		self.frame = None

	def __del__(self):

		self.destroy()

	def is_valid(self):
		return self._handle

	def is_frame_initialized(self):
		return self.frame

	def handle(self):
		return self._handle

	def destroy(self):
		if self.is_valid():
			_k4abt.k4abt_tracker_destroy(self._handle)
			self._handle = None

	def update(self, capture=None, timeout_in_ms=K4A_WAIT_INFINITE):
		# Add capture to the body tracker processing queue
		if capture:
			self.enqueue_capture(capture.handle(), timeout_in_ms)
		else:
			self.enqueue_capture(Device.capture.handle(), timeout_in_ms)

		return self.pop_result(timeout_in_ms)

	def enqueue_capture(self, capture_handle, timeout_in_ms=K4A_WAIT_INFINITE):
		_k4abt.VERIFY(_k4abt.k4abt_tracker_enqueue_capture(self._handle, capture_handle, timeout_in_ms), "Body tracker capture enqueue failed!")

	def pop_result(self, timeout_in_ms=K4A_WAIT_INFINITE):

		if self.is_frame_initialized():
			self.frame.release()
			_k4abt.VERIFY(_k4abt.k4abt_tracker_pop_result(self._handle, self.frame.handle(), timeout_in_ms), "Body tracker get body frame failed!")
		else:
			frame_handle = _k4abt.k4abt_frame_t()
			_k4abt.VERIFY(_k4abt.k4abt_tracker_pop_result(self._handle, frame_handle, timeout_in_ms), "Body tracker get body frame failed!")
			self.frame = Frame(frame_handle, self.calibration)

		return self.frame

	def set_temporal_smoothing(self, smoothing_factor):
		_k4abt.k4abt_tracker_set_temporal_smoothing(self._handle, smoothing_factor)

	def shutdown(self):
		_k4abt.k4abt_tracker_shutdown(self._handle)

	def create(self, model_type):

		tracker_config = self.get_tracker_configuration(model_type)

		tracker_handle = _k4abt.k4abt_tracker_t()
		_k4abt.VERIFY(_k4abt.k4abt_tracker_create(self.calibration.handle(), tracker_config, tracker_handle), "Body tracker initialization failed!")
		
		return tracker_handle

	def get_tracker_configuration(self, model_type):
		tracker_config = k4abt_tracker_default_configuration

		if model_type == _k4abt.K4ABT_LITE_MODEL:
			tracker_config.model_path = get_k4abt_lite_model_path()

		return tracker_config


