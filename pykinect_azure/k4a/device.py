import ctypes
from ctypes import byref
from pykinect_azure.k4a import _k4a
from pykinect_azure.k4a.capture import Capture
from pykinect_azure.k4a.imu_sample import ImuSample
from pykinect_azure.k4a.calibration import Calibration
from pykinect_azure.k4a.configuration import Configuration
from pykinect_azure.k4arecord.record import Record
from pykinect_azure.k4a._k4atypes import K4A_WAIT_INFINITE

class Device:
	calibration = None
	capture = None
	imu_sample = None

	def __init__(self, index=0):
		self._handle = None
		self._handle = self.open(index)
		self.recording = False

	def __del__(self):
		self.close()

	def is_valid(self):
		return self._handle

	def is_capture_initialized(self):
		return self.capture

	def is_imu_sample_initialized(self):
		return self.imu_sample

	def handle(self):
		return self._handle

	def start(self, configuration, record=False, record_filepath="output.mkv"):
		self.configuration = configuration
		self.start_cameras(configuration)
		self.start_imu()

		if record:
			self.record = Record(self._handle, self.configuration.handle(), record_filepath)
			self.recording = True

	def close(self):
		if self.is_valid():
			self.stop_imu()
			self.stop_cameras()
			_k4a.k4a_device_close(self._handle)

			# Clear members
			self._handle = None
			self.record = None
			self.recording = False

	def update(self, timeout_in_ms=K4A_WAIT_INFINITE):
		# Get cameras capture
		capture_handle = self.get_capture(timeout_in_ms)

		if self.is_capture_initialized():
			self.capture._handle = capture_handle
		else :
			self.capture = Capture(capture_handle, self.calibration)
		
		# Write capture if recording
		if self.recording:
			self.record.write_capture(self.capture.handle())
			
		return self.capture

	def update_imu(self, timeout_in_ms=K4A_WAIT_INFINITE):
		
		# Get imu sample
		imu_sample = self.get_imu_sample(timeout_in_ms)

		if self.is_imu_sample_initialized():
			self.imu_sample._struct = imu_sample
			self.imu_sample.parse_data()
		else :
			self.imu_sample = ImuSample(imu_sample)
				
		return self.imu_sample

	def get_capture(self, timeout_in_ms=_k4a.K4A_WAIT_INFINITE):

		# Release current handle
		if self.is_capture_initialized():
			self.capture.release_handle()

		capture_handle = _k4a.k4a_capture_t()
		_k4a.VERIFY(_k4a.k4a_device_get_capture(self._handle, capture_handle, timeout_in_ms),"Get capture failed!")
			
		return capture_handle

	def get_imu_sample(self, timeout_in_ms=_k4a.K4A_WAIT_INFINITE):

		imu_sample = _k4a.k4a_imu_sample_t()

		_k4a.VERIFY(_k4a.k4a_device_get_imu_sample(self._handle,imu_sample,timeout_in_ms),"Get IMU failed!")

		return imu_sample

	def start_cameras(self, device_config):
		self.calibration = self.get_calibration(device_config.depth_mode, device_config.color_resolution)

		_k4a.VERIFY(_k4a.k4a_device_start_cameras(self._handle, device_config.handle()),"Start K4A cameras failed!")

	def stop_cameras(self):

		_k4a.k4a_device_stop_cameras(self._handle)

	def start_imu(self):

		_k4a.VERIFY(_k4a.k4a_device_start_imu(self._handle),"Start K4A IMU failed!")

	def stop_imu(self):

		_k4a.k4a_device_stop_imu(self._handle)

	def get_serialnum(self):

		serial_number_size = ctypes.c_size_t()
		result = _k4a.k4a_device_get_serialnum(self._handle, None, serial_number_size)

		if result == _k4a.K4A_BUFFER_RESULT_TOO_SMALL:
			serial_number = ctypes.create_string_buffer(serial_number_size.value)

		_k4a.VERIFY(_k4a.k4a_device_get_serialnum(self._handle,serial_number,serial_number_size),"Read serial number failed!")

		return serial_number.value.decode("utf-8") 

	def get_calibration(self, depth_mode, color_resolution):   
        
		calibration_handle = _k4a.k4a_calibration_t()

		_k4a.VERIFY(_k4a.k4a_device_get_calibration(self._handle,depth_mode,color_resolution,calibration_handle),"Get calibration failed!")
		
		return Calibration(calibration_handle)

	def get_version(self):

		version = _k4a.k4a_hardware_version_t()

		_k4a.VERIFY(_k4a.k4a_device_get_version(self._handle,version),"Get version failed!")

		return version

	def device_configinit(self):
 		# Automatically determine master and Sub devices and config		
		device_config = Configuration()
		device_config.color_format = _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
		device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
		device_config.depth_mode = _k4a.K4A_DEPTH_MODE_NFOV_2X2BINNED
		device_config.calibration_type = _k4a.K4A_CALIBRATION_TYPE_COLOR
		device_config.synchronized_images_only = True
		
		sync_in_connected = ctypes.c_bool()
		sync_out_connected = ctypes.c_bool()
		
		if _k4a.K4A_RESULT_SUCCEEDED == _k4a.k4a_device_get_sync_jack(self.handle(), byref(sync_in_connected), byref(sync_out_connected)):
			if sync_in_connected and not sync_out_connected:
				device_config.wired_sync_mode = _k4a.K4A_WIRED_SYNC_MODE_SUBORDINATE
				device_config.subordinate_delay_off_master_usec = 160
				device_type = "Sub"
			elif not sync_in_connected and sync_out_connected:
				device_config.wired_sync_mode = _k4a.K4A_WIRED_SYNC_MODE_MASTER
				device_type = "Master"
			elif sync_in_connected and sync_out_connected:
				device_config.wired_sync_mode = _k4a.K4A_WIRED_SYNC_MODE_SUBORDINATE
				device_config.subordinate_delay_off_master_usec = 160
				device_type = "Sub"
			else:
				device_config.wired_sync_mode = _k4a.K4A_WIRED_SYNC_MODE_STANDALONE
				device_type = "Standalone"
		else:
			device_config.wired_sync_mode = _k4a.K4A_WIRED_SYNC_MODE_STANDALONE
			device_type = "Standalone"
		
		return device_config, device_type
					  		
	@staticmethod
	def open(index=0):
		device_handle = _k4a.k4a_device_t()
		
		_k4a.VERIFY(_k4a.k4a_device_open(index, device_handle),"Open K4A Device failed!")

		return device_handle

	@staticmethod
	def device_get_installed_count():
		return int(_k4a.k4a_device_get_installed_count())

