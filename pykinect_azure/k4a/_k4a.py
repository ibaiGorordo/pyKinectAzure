import ctypes
import sys
import traceback
from pykinect_azure.k4a._k4atypes import *

k4a_dll = None

def setup_library(module_k4a_path):

	global k4a_dll

	try: 
		k4a_dll = ctypes.CDLL(module_k4a_path)

	except Exception as e:
		print("Failed to load library", e)
		sys.exit(1)

def k4a_device_get_installed_count():
	#K4A_EXPORT uint32_t k4a_device_get_installed_count(void);

	return k4a_dll.k4a_device_get_installed_count()

def k4a_device_open(device_id, device_handle):
	#K4A_EXPORT k4a_result_t k4a_device_open(uint32_t index, k4a_device_t *device_handle);

	_k4a_device_open = k4a_dll.k4a_device_open
	_k4a_device_open.restype=ctypes.c_int
	_k4a_device_open.argtypes=(ctypes.c_uint32, ctypes.POINTER(k4a_device_t))

	return _k4a_device_open(device_id, device_handle)
	
def k4a_device_close(device_handle):
	#K4A_EXPORT void k4a_device_close(k4a_device_t device_handle);

	_k4a_device_close = k4a_dll.k4a_device_close
	_k4a_device_close.restype=None
	_k4a_device_close.argtypes=(k4a_device_t,)
	_k4a_device_close(device_handle)

def k4a_device_get_capture(device_handle, capture_handle, timeout):
	"""
	K4A_EXPORT k4a_wait_result_t k4a_device_get_capture(k4a_device_t device_handle,
														k4a_capture_t *capture_handle,
														int32_t timeout_in_ms);
	"""

	_k4a_device_get_capture = k4a_dll.k4a_device_get_capture
	_k4a_device_get_capture.restype=ctypes.c_int
	_k4a_device_get_capture.argtypes=(k4a_device_t, ctypes.POINTER(k4a_capture_t), ctypes.c_int32)

	return _k4a_device_get_capture(device_handle, capture_handle, timeout)

def k4a_device_get_imu_sample(device_handle, imu_sample_handle, timeout):
	"""
	K4A_EXPORT k4a_wait_result_t k4a_device_get_imu_sample(k4a_device_t device_handle,
															k4a_imu_sample_t *imu_sample,
															int32_t timeout_in_ms);
	"""

	_k4a_device_get_imu_sample = k4a_dll.k4a_device_get_imu_sample
	_k4a_device_get_imu_sample.restype=ctypes.c_int
	_k4a_device_get_imu_sample.argtypes=(k4a_device_t, ctypes.POINTER(k4a_imu_sample_t), ctypes.c_int32)

	return _k4a_device_get_imu_sample(device_handle, imu_sample_handle, timeout)

def k4a_capture_create(capture_handle):
	#K4A_EXPORT k4a_result_t k4a_capture_create(k4a_capture_t *capture_handle);

	_k4a_capture_create = k4a_dll.k4a_capture_create
	_k4a_capture_create.restype= k4a_result_t
	_k4a_capture_create.argtypes=(ctypes.POINTER(k4a_capture_t), )

	return _k4a_capture_create(capture_handle)

def k4a_capture_release(capture_handle):
	#K4A_EXPORT void k4a_capture_release(k4a_capture_t capture_handle);

	_k4a_capture_release = k4a_dll.k4a_capture_release
	_k4a_capture_release.restype = None
	_k4a_capture_release.argtypes=(k4a_capture_t,)

	_k4a_capture_release(capture_handle)

def k4a_capture_reference(capture_handle):
	#K4A_EXPORT void k4a_capture_reference(k4a_capture_t capture_handle);

	_k4a_capture_reference = k4a_dll.k4a_capture_reference
	_k4a_capture_reference.restype = None
	_k4a_capture_reference.argtypes=(k4a_capture_t,)

	_k4a_capture_reference(capture_handle)

def k4a_capture_get_color_image(capture_handle):
	#K4A_EXPORT k4a_image_t k4a_capture_get_color_image(k4a_capture_t capture_handle)

	_k4a_capture_get_color_image = k4a_dll.k4a_capture_get_color_image
	_k4a_capture_get_color_image.restype=k4a_image_t
	_k4a_capture_get_color_image.argtypes=(k4a_capture_t,)

	return _k4a_capture_get_color_image(capture_handle)

def k4a_capture_get_depth_image(capture_handle):
	#K4A_EXPORT k4a_image_t k4a_capture_get_depth_image(k4a_capture_t capture_handle);

	_k4a_capture_get_depth_image = k4a_dll.k4a_capture_get_depth_image
	_k4a_capture_get_depth_image.restype=k4a_image_t
	_k4a_capture_get_depth_image.argtypes=(k4a_capture_t,)

	return _k4a_capture_get_depth_image(capture_handle)

def k4a_capture_get_ir_image(capture_handle):
	#K4A_EXPORT k4a_image_t k4a_capture_get_ir_image(k4a_capture_t capture_handle);

	_k4a_capture_get_ir_image = k4a_dll.k4a_capture_get_ir_image
	_k4a_capture_get_ir_image.restype=k4a_image_t
	_k4a_capture_get_ir_image.argtypes=(k4a_capture_t,)

	return _k4a_capture_get_ir_image(capture_handle)

def k4a_capture_set_color_image(capture_handle, image_handle):
	#K4A_EXPORT void k4a_capture_set_color_image(k4a_capture_t capture_handle, k4a_image_t image_handle);

	_k4a_capture_set_color_image = k4a_dll.k4a_capture_set_color_image
	_k4a_capture_set_color_image.restype=None
	_k4a_capture_set_color_image.argtypes=(k4a_capture_t,k4a_image_t,)
	
	_k4a_capture_set_color_image(capture_handle, image_handle)

def k4a_capture_set_depth_image(capture_handle, image_handle):
	#K4A_EXPORT void k4a_capture_set_depth_image(k4a_capture_t capture_handle, k4a_image_t image_handle);

	_k4a_capture_set_depth_image = k4a_dll.k4a_capture_set_depth_image
	_k4a_capture_set_depth_image.restype=None
	_k4a_capture_set_depth_image.argtypes=(k4a_capture_t,k4a_image_t,)
	
	_k4a_capture_set_depth_image(capture_handle, image_handle)

def k4a_capture_set_ir_image(capture_handle, image_handle):
	#K4A_EXPORT void k4a_capture_set_ir_image(k4a_capture_t capture_handle, k4a_image_t image_handle);

	_k4a_capture_set_ir_image = k4a_dll.k4a_capture_set_ir_image
	_k4a_capture_set_ir_image.restype=None
	_k4a_capture_set_ir_image.argtypes=(k4a_capture_t,k4a_image_t,)
	
	_k4a_capture_set_ir_image(capture_handle, image_handle)

def k4a_capture_set_temperature_c(capture_handle, temperature):
	#K4A_EXPORT void k4a_capture_set_temperature_c(k4a_capture_t capture_handle, float temperature_c);

	_k4a_capture_set_temperature_c = k4a_dll.k4a_capture_set_temperature_c
	_k4a_capture_set_temperature_c.restype=None
	_k4a_capture_set_temperature_c.argtypes=(k4a_capture_t,ctypes.c_float,)
	
	_k4a_capture_set_temperature_c(capture_handle, temperature)

def k4a_capture_get_temperature_c(capture_handle):
	#K4A_EXPORT float k4a_capture_get_temperature_c(k4a_capture_t capture_handle);

	_k4a_capture_get_temperature_c = k4a_dll.k4a_capture_get_temperature_c
	_k4a_capture_get_temperature_c.restype=ctypes.c_float
	_k4a_capture_get_temperature_c.argtypes=(k4a_capture_t, )

	return _k4a_capture_get_temperature_c(capture_handle)

def k4a_image_create(image_format, width, height, stride, image_handle):
	"""
	K4A_EXPORT k4a_result_t k4a_image_create(k4a_image_format_t format,
												int width_pixels,
												int height_pixels,
												int stride_bytes,
												k4a_image_t *image_handle);
	"""
	_k4a_image_create = k4a_dll.k4a_image_create
	_k4a_image_create.restype=k4a_result_t
	_k4a_image_create.argtypes=(k4a_image_format_t,\
									ctypes.c_int,\
									ctypes.c_int,\
									ctypes.c_int,\
									ctypes.POINTER(k4a_image_t),)

	return _k4a_image_create(image_format, width, height, stride, image_handle)

def k4a_image_create_from_buffer(image_format, width, height, stride, buffer, buffer_size, buffer_release_cb, buffer_release_cb_context, image_handle):
	"""
		K4A_EXPORT k4a_result_t k4a_image_create_from_buffer(k4a_image_format_t format,
																int width_pixels,
																int height_pixels,
																int stride_bytes,
																uint8_t *buffer,
																size_t buffer_size,
																k4a_memory_destroy_cb_t *buffer_release_cb,
																void *buffer_release_cb_context,
																k4a_image_t *image_handle);
	"""
	_k4a_image_create_from_buffer = k4a_dll.k4a_image_create_from_buffer
	_k4a_image_create_from_buffer.restype=k4a_result_t
	_k4a_image_create_from_buffer.argtypes=(k4a_image_format_t,\
												ctypes.c_int,\
												ctypes.c_int,\
												ctypes.c_int,\
												ctypes.POINTER(ctypes.c_uint8),\
												ctypes.c_size_t,\
												ctypes.c_void_p,\
												ctypes.c_void_p,\
												ctypes.POINTER(k4a_image_t),)

	return _k4a_image_create_from_buffer(image_format, width, height, stride, buffer, buffer_size, buffer_release_cb, buffer_release_cb_context, image_handle)

def k4a_image_get_buffer(image_handle):
	#K4A_EXPORT uint8_t *k4a_image_get_buffer(k4a_image_t image_handle);
	
	_k4a_image_get_buffer = k4a_dll.k4a_image_get_buffer
	_k4a_image_get_buffer.restype=ctypes.POINTER(ctypes.c_uint8)
	_k4a_image_get_buffer.argtypes=(k4a_image_t, )

	return _k4a_image_get_buffer(image_handle)

def k4a_image_get_size(image_handle):
	#K4A_EXPORT size_t k4a_image_get_size(k4a_image_t image_handle);

	_k4a_image_get_size = k4a_dll.k4a_image_get_size
	_k4a_image_get_size.restype=ctypes.c_size_t
	_k4a_image_get_size.argtypes=(k4a_image_t, )

	return _k4a_image_get_size(image_handle)	

def k4a_image_get_format(image_handle):
	#K4A_EXPORT k4a_image_format_t k4a_image_get_format(k4a_image_t image_handle);

	_k4a_image_get_format = k4a_dll.k4a_image_get_format
	_k4a_image_get_format.restype=k4a_image_format_t
	_k4a_image_get_format.argtypes=(k4a_image_t, )

	return _k4a_image_get_format(image_handle)			

def k4a_image_get_width_pixels(image_handle):
	#K4A_EXPORT int k4a_image_get_width_pixels(k4a_image_t image_handle);

	_k4a_image_get_width_pixels = k4a_dll.k4a_image_get_width_pixels
	_k4a_image_get_width_pixels.restype=ctypes.c_int
	_k4a_image_get_width_pixels.argtypes=(k4a_image_t, )

	return _k4a_image_get_width_pixels(image_handle)	

def k4a_image_get_height_pixels(image_handle):
	#K4A_EXPORT int k4a_image_get_height_pixels(k4a_image_t image_handle);

	_k4a_image_get_height_pixels = k4a_dll.k4a_image_get_height_pixels
	_k4a_image_get_height_pixels.restype=ctypes.c_int
	_k4a_image_get_height_pixels.argtypes=(k4a_image_t, )

	return _k4a_image_get_height_pixels(image_handle)	
	
def k4a_image_get_stride_bytes(image_handle):
	#K4A_EXPORT int k4a_image_get_stride_bytes(k4a_image_t image_handle);

	_k4a_image_get_stride_bytes = k4a_dll.k4a_image_get_stride_bytes
	_k4a_image_get_stride_bytes.restype=ctypes.c_int
	_k4a_image_get_stride_bytes.argtypes=(k4a_image_t, )

	return _k4a_image_get_stride_bytes(image_handle)	

def k4a_image_get_timestamp_usec(image_handle):
	#K4A_DEPRECATED_EXPORT uint64_t k4a_image_get_timestamp_usec(k4a_image_t image_handle);

	_k4a_image_get_timestamp_usec = k4a_dll.k4a_image_get_timestamp_usec
	_k4a_image_get_timestamp_usec.restype=ctypes.c_uint64
	_k4a_image_get_timestamp_usec.argtypes=(k4a_image_t, )

	return _k4a_image_get_timestamp_usec(image_handle)		

def k4a_image_get_device_timestamp_usec(image_handle):
	#K4A_EXPORT uint64_t k4a_image_get_device_timestamp_usec(k4a_image_t image_handle);

	_k4a_image_get_device_timestamp_usec = k4a_dll.k4a_image_get_device_timestamp_usec
	_k4a_image_get_device_timestamp_usec.restype=ctypes.c_uint64
	_k4a_image_get_device_timestamp_usec.argtypes=(k4a_image_t, )

	return _k4a_image_get_device_timestamp_usec(image_handle)	

def k4a_image_get_system_timestamp_nsec(image_handle):
	#K4A_EXPORT uint64_t k4a_image_get_system_timestamp_nsec(k4a_image_t image_handle);

	_k4a_image_get_system_timestamp_nsec = k4a_dll.k4a_image_get_system_timestamp_nsec
	_k4a_image_get_system_timestamp_nsec.restype=ctypes.c_uint64
	_k4a_image_get_system_timestamp_nsec.argtypes=(k4a_image_t, )

	return _k4a_image_get_system_timestamp_nsec(image_handle)

def k4a_image_get_exposure_usec(image_handle):
	#K4A_EXPORT uint64_t k4a_image_get_exposure_usec(k4a_image_t image_handle);

	_k4a_image_get_exposure_usec = k4a_dll.k4a_image_get_exposure_usec
	_k4a_image_get_exposure_usec.restype=ctypes.c_uint64
	_k4a_image_get_exposure_usec.argtypes=(k4a_image_t, )

	return _k4a_image_get_exposure_usec(image_handle)	

def k4a_image_get_white_balance(image_handle):
	#K4A_EXPORT uint32_t k4a_image_get_white_balance(k4a_image_t image_handle);

	_k4a_image_get_white_balance = k4a_dll.k4a_image_get_white_balance
	_k4a_image_get_white_balance.restype=ctypes.c_uint32
	_k4a_image_get_white_balance.argtypes=(k4a_image_t, )

	return _k4a_image_get_white_balance(image_handle)	

def k4a_image_get_iso_speed(image_handle):
	#K4A_EXPORT uint32_t k4a_image_get_iso_speed(k4a_image_t image_handle);

	_k4a_image_get_iso_speed = k4a_dll.k4a_image_get_iso_speed
	_k4a_image_get_iso_speed.restype=ctypes.c_uint32
	_k4a_image_get_iso_speed.argtypes=(k4a_image_t, )

	return _k4a_image_get_iso_speed(image_handle)	

def k4a_image_set_device_timestamp_usec(image_handle, timestamp_usec):
	#K4A_EXPORT void k4a_image_set_device_timestamp_usec(k4a_image_t image_handle, uint64_t timestamp_usec);

	_k4a_image_set_device_timestamp_usec = k4a_dll.k4a_image_set_device_timestamp_usec
	_k4a_image_set_device_timestamp_usec.restype=None
	_k4a_image_set_device_timestamp_usec.argtypes=(k4a_image_t, ctypes.c_uint64,)

	_k4a_image_set_device_timestamp_usec(image_handle, timestamp_usec)		

def k4a_image_set_timestamp_usec(image_handle, timestamp_usec):
	#K4A_DEPRECATED_EXPORT void k4a_image_set_timestamp_usec(k4a_image_t image_handle, uint64_t timestamp_usec);

	_k4a_image_set_timestamp_usec = k4a_dll.k4a_image_set_timestamp_usec
	_k4a_image_set_timestamp_usec.restype=None
	_k4a_image_set_timestamp_usec.argtypes=(k4a_image_t, ctypes.c_uint64,)

	_k4a_image_set_timestamp_usec(image_handle, timestamp_usec)

def k4a_image_set_system_timestamp_nsec(image_handle, timestamp_nsec):
	#K4A_EXPORT void k4a_image_set_system_timestamp_nsec(k4a_image_t image_handle, uint64_t timestamp_nsec);

	_k4a_image_set_system_timestamp_nsec = k4a_dll.k4a_image_set_system_timestamp_nsec
	_k4a_image_set_system_timestamp_nsec.restype=None
	_k4a_image_set_system_timestamp_nsec.argtypes=(k4a_image_t, ctypes.c_uint64,)

	_k4a_image_set_system_timestamp_nsec(image_handle, timestamp_nsec)

def k4a_image_set_exposure_usec(image_handle, exposure_usec):
	#K4A_EXPORT void k4a_image_set_exposure_usec(k4a_image_t image_handle, uint64_t exposure_usec);

	_k4a_image_set_exposure_usec = k4a_dll.k4a_image_set_exposure_usec
	_k4a_image_set_exposure_usec.restype=None
	_k4a_image_set_exposure_usec.argtypes=(k4a_image_t, ctypes.c_uint64,)

	_k4a_image_set_exposure_usec(image_handle, exposure_usec)

def k4a_image_set_exposure_time_usec(image_handle, exposure_usec):
	#K4A_DEPRECATED_EXPORT void k4a_image_set_exposure_time_usec(k4a_image_t image_handle, uint64_t exposure_usec);

	_k4a_image_set_exposure_time_usec = k4a_dll.k4a_image_set_exposure_time_usec
	_k4a_image_set_exposure_time_usec.restype=None
	_k4a_image_set_exposure_time_usec.argtypes=(k4a_image_t, ctypes.c_uint64,)

	_k4a_image_set_exposure_time_usec(image_handle, exposure_usec)

def k4a_image_set_white_balance(image_handle, white_balance):
	#K4A_EXPORT void k4a_image_set_white_balance(k4a_image_t image_handle, uint32_t white_balance);

	_k4a_image_set_white_balance = k4a_dll.k4a_image_set_white_balance
	_k4a_image_set_white_balance.restype=None
	_k4a_image_set_white_balance.argtypes=(k4a_image_t, ctypes.c_uint32,)

	_k4a_image_set_white_balance(image_handle, white_balance)

def k4a_image_set_iso_speed(image_handle, iso_speed):
	#K4A_EXPORT void k4a_image_set_iso_speed(k4a_image_t image_handle, uint32_t iso_speed);

	_k4a_image_set_iso_speed = k4a_dll.k4a_image_set_iso_speed
	_k4a_image_set_iso_speed.restype=None
	_k4a_image_set_iso_speed.argtypes=(k4a_image_t, ctypes.c_uint32,)

	_k4a_image_set_iso_speed(image_handle, iso_speed)

def k4a_image_reference(image_handle):
	#K4A_EXPORT void k4a_image_reference(k4a_image_t image_handle);

	_k4a_image_reference = k4a_dll.k4a_image_reference
	_k4a_image_reference.restype=None
	_k4a_image_reference.argtypes=(k4a_image_t,)

	_k4a_image_reference(image_handle)

def k4a_image_release(image_handle):
	#K4A_EXPORT void k4a_image_release(k4a_image_t image_handle);

	_k4a_image_release = k4a_dll.k4a_image_release
	_k4a_image_release.restype=None
	_k4a_image_release.argtypes=(k4a_image_t,)

	_k4a_image_release(image_handle)

def k4a_device_start_cameras(device_handle, config):
	#K4A_EXPORT k4a_result_t k4a_device_start_cameras(k4a_device_t device_handle, const k4a_device_configuration_t *config);

	_k4a_device_start_cameras = k4a_dll.k4a_device_start_cameras
	_k4a_device_start_cameras.restype=k4a_result_t
	_k4a_device_start_cameras.argtypes=(k4a_device_t, ctypes.POINTER(k4a_device_configuration_t),)

	return _k4a_device_start_cameras(device_handle, config)

def k4a_device_stop_cameras(device_handle):
	#K4A_EXPORT void k4a_device_stop_cameras(k4a_device_t device_handle);

	_k4a_device_stop_cameras = k4a_dll.k4a_device_stop_cameras
	_k4a_device_stop_cameras.restype=None
	_k4a_device_stop_cameras.argtypes=(k4a_device_t,)

	_k4a_device_stop_cameras(device_handle)
	

def k4a_device_start_imu(device_handle):
	#K4A_EXPORT k4a_result_t k4a_device_start_imu(k4a_device_t device_handle);

	_k4a_device_start_imu = k4a_dll.k4a_device_start_imu
	_k4a_device_start_imu.restype=k4a_result_t
	_k4a_device_start_imu.argtypes=(k4a_device_t,)

	return _k4a_device_start_imu(device_handle)

def k4a_device_stop_imu(device_handle):
	#K4A_EXPORT void k4a_device_stop_imu(k4a_device_t device_handle);

	_k4a_device_stop_imu = k4a_dll.k4a_device_stop_imu
	_k4a_device_stop_imu.restype=None
	_k4a_device_stop_imu.argtypes=(k4a_device_t,)

	_k4a_device_stop_imu(device_handle)
	
def k4a_device_get_serialnum(device_handle, serial_number, serial_number_size):
	"""
	K4A_EXPORT k4a_buffer_result_t k4a_device_get_serialnum(k4a_device_t device_handle,
															char *serial_number,
															size_t *serial_number_size);
	"""

	_k4a_device_get_serialnum = k4a_dll.k4a_device_get_serialnum
	_k4a_device_get_serialnum.restype=k4a_buffer_result_t
	_k4a_device_get_serialnum.argtypes=(k4a_device_t,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t))

	return _k4a_device_get_serialnum(device_handle, serial_number, serial_number_size)
	
def k4a_device_get_version(device_handle, hardware_version):
	#K4A_EXPORT k4a_result_t k4a_device_get_version(k4a_device_t device_handle, k4a_hardware_version_t *version);

	_k4a_device_get_version = k4a_dll.k4a_device_get_version
	_k4a_device_get_version.restype=k4a_result_t
	_k4a_device_get_version.argtypes=(k4a_device_t,ctypes.POINTER(k4a_hardware_version_t),)

	return _k4a_device_get_version(device_handle, hardware_version)

def k4a_device_get_color_control_capabilities(device_handle, command, supports_auto, min_value, max_value, step_value, default_value, default_mode):
	"""
	K4A_EXPORT k4a_result_t k4a_device_get_color_control_capabilities(k4a_device_t device_handle,
																		k4a_color_control_command_t command,
																		bool *supports_auto,
																		int32_t *min_value,
																		int32_t *max_value,
																		int32_t *step_value,
																		int32_t *default_value,
																		k4a_color_control_mode_t *default_mode);
	"""

	_k4a_device_get_color_control_capabilities = k4a_dll.k4a_device_get_color_control_capabilities
	_k4a_device_get_color_control_capabilities.restype=k4a_result_t
	_k4a_device_get_color_control_capabilities.argtypes=(k4a_device_t,\
															k4a_color_control_command_t,\
															ctypes.POINTER(ctypes.c_bool),\
															ctypes.POINTER(ctypes.c_int32),\
															ctypes.POINTER(ctypes.c_int32),\
															ctypes.POINTER(ctypes.c_int32),\
															ctypes.POINTER(ctypes.c_int32),\
															ctypes.POINTER(k4a_color_control_mode_t),\
															)

	return _k4a_device_get_color_control_capabilities(device_handle, command, supports_auto, min_value, max_value, step_value, default_value, default_mode)

def k4a_device_get_color_control(device_handle, command, mode, value):
	"""
	K4A_EXPORT k4a_result_t k4a_device_get_color_control(k4a_device_t device_handle,
															k4a_color_control_command_t command,
															k4a_color_control_mode_t *mode,
															int32_t *value);
	"""

	_k4a_device_get_color_control = k4a_dll.k4a_device_get_color_control
	_k4a_device_get_color_control.restype=k4a_result_t
	_k4a_device_get_color_control.argtypes=(k4a_device_t,\
												k4a_color_control_command_t,\
												ctypes.POINTER(k4a_color_control_mode_t),\
												ctypes.POINTER(ctypes.c_int32),\
												)

	return _k4a_device_get_color_control(device_handle, command, mode, value)
	
def k4a_device_set_color_control(device_handle, command, mode, value):
	"""
	K4A_EXPORT k4a_result_t k4a_device_set_color_control(k4a_device_t device_handle,
															k4a_color_control_command_t command,
															k4a_color_control_mode_t mode,
															int32_t value);
	"""

	_k4a_device_set_color_control = k4a_dll.k4a_device_set_color_control
	_k4a_device_set_color_control.restype=k4a_result_t
	_k4a_device_set_color_control.argtypes=(k4a_device_t,\
												k4a_color_control_command_t,\
												k4a_color_control_mode_t,\
												ctypes.c_int32,\
												)

	return _k4a_device_set_color_control(device_handle, command, mode, value)

def k4a_device_get_raw_calibration(device_handle, data, data_size):
	"""
	K4A_EXPORT k4a_buffer_result_t k4a_device_get_raw_calibration(k4a_device_t device_handle,
																	uint8_t *data,
																	size_t *data_size);
	"""

	_k4a_device_get_raw_calibration = k4a_dll.k4a_device_get_raw_calibration
	_k4a_device_get_raw_calibration.restype=k4a_buffer_result_t
	_k4a_device_get_raw_calibration.argtypes=(k4a_device_t,\
													ctypes.POINTER(ctypes.c_uint8),\
													ctypes.POINTER(ctypes.c_size_t),\
													)

	return _k4a_device_get_raw_calibration(device_handle, data, data_size)

def k4a_device_get_calibration(device_handle, depth_mode, color_resolution, calibration):
	"""
	K4A_EXPORT k4a_result_t k4a_device_get_calibration(k4a_device_t device_handle,
														const k4a_depth_mode_t depth_mode,
														const k4a_color_resolution_t color_resolution,
														k4a_calibration_t *calibration);
	"""

	_k4a_device_get_calibration = k4a_dll.k4a_device_get_calibration
	_k4a_device_get_calibration.restype=k4a_result_t
	_k4a_device_get_calibration.argtypes=(k4a_device_t, \
												k4a_depth_mode_t, \
												k4a_color_resolution_t, \
												ctypes.POINTER(k4a_calibration_t),\
												)

	return _k4a_device_get_calibration(device_handle, depth_mode, color_resolution, calibration)
		
def k4a_device_get_sync_jack(device_handle, sync_in_jack_connected, sync_out_jack_connected):
	"""
	K4A_EXPORT k4a_result_t k4a_device_get_sync_jack(k4a_device_t device_handle,
														bool *sync_in_jack_connected,
														bool *sync_out_jack_connected);
	"""

	_k4a_device_get_sync_jack = k4a_dll.k4a_device_get_sync_jack
	_k4a_device_get_sync_jack.restype=k4a_result_t
	_k4a_device_get_sync_jack.argtypes=(k4a_device_t, \
											ctypes.POINTER(ctypes.c_bool),\
											ctypes.POINTER(ctypes.c_bool),\
											)

	return _k4a_device_get_sync_jack(device_handle, sync_in_jack_connected, sync_out_jack_connected)
	
def k4a_calibration_get_from_raw(raw_calibration, raw_calibration_size, depth_mode, color_resolution, calibration):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_get_from_raw(char *raw_calibration,
															size_t raw_calibration_size,
															const k4a_depth_mode_t depth_mode,
															const k4a_color_resolution_t color_resolution,
															k4a_calibration_t *calibration);
	"""

	_k4a_calibration_get_from_raw = k4a_dll.k4a_calibration_get_from_raw
	_k4a_calibration_get_from_raw.restype=k4a_result_t
	_k4a_calibration_get_from_raw.argtypes=(ctypes.POINTER(ctypes.c_char), \
												ctypes.c_size_t,\
												k4a_depth_mode_t,\
												k4a_color_resolution_t,\
												ctypes.POINTER(k4a_calibration_t),\
												)

	return _k4a_calibration_get_from_raw(raw_calibration, raw_calibration_size, depth_mode, color_resolution, calibration)

def k4a_calibration_3d_to_3d(calibration, source_point3d_mm, source_camera, target_camera, target_point3d_mm):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_3d_to_3d(const k4a_calibration_t *calibration,
														const k4a_float3_t *source_point3d_mm,
														const k4a_calibration_type_t source_camera,
														const k4a_calibration_type_t target_camera,
														k4a_float3_t *target_point3d_mm);
	"""

	_k4a_calibration_3d_to_3d = k4a_dll.k4a_calibration_3d_to_3d
	_k4a_calibration_3d_to_3d.restype=k4a_result_t
	_k4a_calibration_3d_to_3d.argtypes=(ctypes.POINTER(k4a_calibration_t), \
											ctypes.POINTER(k4a_float3_t), \
											k4a_calibration_type_t,\
											k4a_calibration_type_t,\
											ctypes.POINTER(k4a_float3_t),\
											)

	return _k4a_calibration_3d_to_3d(calibration, source_point3d_mm, source_camera, target_camera, target_point3d_mm)
	
def k4a_calibration_2d_to_3d(calibration, source_point2d, source_depth_mm, source_camera, target_camera, target_point3d_mm, valid):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_2d_to_3d(const k4a_calibration_t *calibration,
														const k4a_float2_t *source_point2d,
														const float source_depth_mm,
														const k4a_calibration_type_t source_camera,
														const k4a_calibration_type_t target_camera,
														k4a_float3_t *target_point3d_mm,
														int *valid);
	"""

	_k4a_calibration_2d_to_3d = k4a_dll.k4a_calibration_2d_to_3d
	_k4a_calibration_2d_to_3d.restype=k4a_result_t
	_k4a_calibration_2d_to_3d.argtypes=(ctypes.POINTER(k4a_calibration_t), \
											ctypes.POINTER(k4a_float2_t), \
											ctypes.c_float,\
											k4a_calibration_type_t,\
											k4a_calibration_type_t,\
											ctypes.POINTER(k4a_float3_t),\
											ctypes.POINTER(ctypes.c_int),\
											)
	
	return _k4a_calibration_2d_to_3d(calibration, source_point2d, source_depth_mm, source_camera, target_camera, target_point3d_mm, valid)

def k4a_calibration_3d_to_2d(calibration, source_point3d_mm, source_camera, target_camera, target_point2d, valid):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_3d_to_2d(const k4a_calibration_t *calibration,
														const k4a_float3_t *source_point3d_mm,
														const k4a_calibration_type_t source_camera,
														const k4a_calibration_type_t target_camera,
														k4a_float2_t *target_point2d,
														int *valid);
	"""

	_k4a_calibration_3d_to_2d = k4a_dll.k4a_calibration_3d_to_2d
	_k4a_calibration_3d_to_2d.restype=k4a_result_t
	_k4a_calibration_3d_to_2d.argtypes=(ctypes.POINTER(k4a_calibration_t), \
											ctypes.POINTER(k4a_float3_t), \
											k4a_calibration_type_t,\
											k4a_calibration_type_t,\
											ctypes.POINTER(k4a_float2_t),\
											ctypes.POINTER(ctypes.c_int),\
											)

	return _k4a_calibration_3d_to_2d(calibration, source_point3d_mm, source_camera, target_camera, target_point2d, valid)	

def k4a_calibration_2d_to_2d(calibration, source_point2d, source_depth_mm, source_camera, target_camera, target_point2d, valid):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_2d_to_2d(const k4a_calibration_t *calibration,
														const k4a_float2_t *source_point2d,
														const float source_depth_mm,
														const k4a_calibration_type_t source_camera,
														const k4a_calibration_type_t target_camera,
														k4a_float2_t *target_point2d,
														int *valid);
	"""

	_k4a_calibration_2d_to_2d = k4a_dll.k4a_calibration_2d_to_2d
	_k4a_calibration_2d_to_2d.restype=k4a_result_t
	_k4a_calibration_2d_to_2d.argtypes=(ctypes.POINTER(k4a_calibration_t), \
											ctypes.POINTER(k4a_float2_t), \
											ctypes.c_float,\
											k4a_calibration_type_t,\
											k4a_calibration_type_t,\
											ctypes.POINTER(k4a_float2_t),\
											ctypes.POINTER(ctypes.c_int),\
											)

	return _k4a_calibration_2d_to_2d(calibration, source_point2d, source_depth_mm, source_camera, target_camera, target_point2d, valid)

def k4a_calibration_color_2d_to_depth_2d(calibration, source_point2d, depth_image, target_point2d, valid):
	"""
	K4A_EXPORT k4a_result_t k4a_calibration_color_2d_to_depth_2d(const k4a_calibration_t *calibration,
																	const k4a_float2_t *source_point2d,
																	const k4a_image_t depth_image,
																	k4a_float2_t *target_point2d,
																	int *valid);
	"""

	_k4a_calibration_color_2d_to_depth_2d = k4a_dll.k4a_calibration_color_2d_to_depth_2d
	_k4a_calibration_color_2d_to_depth_2d.restype=k4a_result_t
	_k4a_calibration_color_2d_to_depth_2d.argtypes=(ctypes.POINTER(k4a_calibration_t), \
														ctypes.POINTER(k4a_float2_t), \
														k4a_image_t,\
														ctypes.POINTER(k4a_float2_t),\
														ctypes.POINTER(ctypes.c_int),\
														)

	return _k4a_calibration_color_2d_to_depth_2d(calibration, source_point2d, depth_image, target_point2d, valid)

def k4a_transformation_create(calibration):
	#K4A_EXPORT k4a_transformation_t k4a_transformation_create(const k4a_calibration_t *calibration);

	_k4a_transformation_create = k4a_dll.k4a_transformation_create
	_k4a_transformation_create.restype=k4a_transformation_t
	_k4a_transformation_create.argtypes=(ctypes.POINTER(k4a_calibration_t),)

	return _k4a_transformation_create(calibration)	

def k4a_transformation_destroy(transformation_handle):
	#K4A_EXPORT void k4a_transformation_destroy(k4a_transformation_t transformation_handle);

	_k4a_transformation_destroy = k4a_dll.k4a_transformation_destroy
	_k4a_transformation_destroy.restype=None
	_k4a_transformation_destroy.argtypes=(k4a_transformation_t,)

	_k4a_transformation_destroy(transformation_handle)	
	
def k4a_transformation_depth_image_to_color_camera(transformation_handle, depth_image, transformed_depth_image):
	"""
	K4A_EXPORT k4a_result_t k4a_transformation_depth_image_to_color_camera(k4a_transformation_t transformation_handle,
																			const k4a_image_t depth_image,
																			k4a_image_t transformed_depth_image);
	"""

	_k4a_transformation_depth_image_to_color_camera = k4a_dll.k4a_transformation_depth_image_to_color_camera
	_k4a_transformation_depth_image_to_color_camera.restype=k4a_result_t
	_k4a_transformation_depth_image_to_color_camera.argtypes=(k4a_transformation_t, \
																	k4a_image_t,\
																	k4a_image_t,\
																	)

	_k4a_transformation_depth_image_to_color_camera(transformation_handle, depth_image, transformed_depth_image)
	
def k4a_transformation_depth_image_to_color_camera_custom(transformation_handle, depth_image, custom_image, transformed_depth_image, transformed_custom_image, interpolation_type, invalid_custom_value):
	"""
	K4A_EXPORT k4a_result_t k4a_transformation_depth_image_to_color_camera_custom(k4a_transformation_t transformation_handle,
															const k4a_image_t depth_image,
															const k4a_image_t custom_image,
															k4a_image_t transformed_depth_image,
															k4a_image_t transformed_custom_image,
															k4a_transformation_interpolation_type_t interpolation_type,
															uint32_t invalid_custom_value);
	"""

	_k4a_transformation_depth_image_to_color_camera_custom = k4a_dll.k4a_transformation_depth_image_to_color_camera_custom
	_k4a_transformation_depth_image_to_color_camera_custom.restype=k4a_result_t
	_k4a_transformation_depth_image_to_color_camera_custom.argtypes=(k4a_transformation_t, \
																		k4a_image_t, \
																		k4a_image_t,\
																		k4a_image_t,\
																		k4a_image_t,\
																		k4a_transformation_interpolation_type_t,\
																		ctypes.c_uint32,\
																		)

	return _k4a_transformation_depth_image_to_color_camera_custom(transformation_handle, depth_image, custom_image, transformed_depth_image, transformed_custom_image, interpolation_type, invalid_custom_value)
	
def k4a_transformation_color_image_to_depth_camera(transformation_handle, depth_image, color_image, transformed_color_image):
	"""
	K4A_EXPORT k4a_result_t k4a_transformation_color_image_to_depth_camera(k4a_transformation_t transformation_handle,
																			const k4a_image_t depth_image,
																			const k4a_image_t color_image,
																			k4a_image_t transformed_color_image);
	"""
	
	_k4a_transformation_color_image_to_depth_camera = k4a_dll.k4a_transformation_color_image_to_depth_camera
	_k4a_transformation_color_image_to_depth_camera.restype=k4a_result_t
	_k4a_transformation_color_image_to_depth_camera.argtypes=(k4a_transformation_t, \
																	k4a_image_t, \
																	k4a_image_t,\
																	k4a_image_t,\
																	)

	return _k4a_transformation_color_image_to_depth_camera(transformation_handle, depth_image, color_image, transformed_color_image)
	
def k4a_transformation_depth_image_to_point_cloud(transformation_handle, depth_image, camera, xyz_image):
	"""
	K4A_EXPORT k4a_result_t k4a_transformation_depth_image_to_point_cloud(k4a_transformation_t transformation_handle,
																			const k4a_image_t depth_image,
																			const k4a_calibration_type_t camera,
																			k4a_image_t xyz_image);
	"""

	_k4a_transformation_depth_image_to_point_cloud = k4a_dll.k4a_transformation_depth_image_to_point_cloud
	_k4a_transformation_depth_image_to_point_cloud.restype=k4a_result_t
	_k4a_transformation_depth_image_to_point_cloud.argtypes=(k4a_transformation_t, \
																k4a_image_t, \
																k4a_calibration_type_t,\
																k4a_image_t,\
																)

	return _k4a_transformation_depth_image_to_point_cloud(transformation_handle, depth_image, camera, xyz_image)
	
def VERIFY(result, error):
	if result != K4A_RESULT_SUCCEEDED:
		print(error)
		# traceback.print_stack()
		sys.exit(1)

