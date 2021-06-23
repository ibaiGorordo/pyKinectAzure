import ctypes
import sys
from _k4arecordTypes import *
from _k4atypes import *
import traceback

class k4arecord:
	def __init__(self, modulePath):
		try:
			recorddll = ctypes.CDLL(modulePath.replace('k4a', 'k4arecord'))
		except Exception as e:
			try:
				recorddll = ctypes.CDLL('k4arecord.so')
			except Exception as ee:
				print("Failed to load library", e, ee)
				sys.exit(1)


		"""
		K4ARECORD_EXPORT k4a_result_t k4a_record_create(const char *path,
													k4a_device_t device,
													const k4a_device_configuration_t device_config,
													k4a_record_t *recording_handle);
		"""

		self.k4a_record_create = recorddll.k4a_record_create
		self.k4a_record_create.restype = k4a_result_t
		self.k4a_record_create.argtypes = (ctypes.POINTER(ctypes.c_char), \
										   k4a_device_t, \
										   k4a_device_configuration_t, \
										   ctypes.POINTER(k4a_record_t),\
										   )

		# K4ARECORD_EXPORT k4a_result_t k4a_record_write_header(k4a_record_t recording_handle);
		self.k4a_record_write_header = recorddll.k4a_record_write_header
		self.k4a_record_write_header.restype = k4a_result_t
		self.k4a_record_write_header.argtypes = (k4a_record_t,)

		# K4ARECORD_EXPORT k4a_result_t k4a_record_write_capture(k4a_record_t recording_handle, k4a_capture_t capture_handle);
		self.k4a_record_write_capture = recorddll.k4a_record_write_capture
		self.k4a_record_write_capture.restype = k4a_result_t
		self.k4a_record_write_capture.argtypes = (k4a_record_t, \
												  k4a_capture_t)

		# K4ARECORD_EXPORT k4a_result_t k4a_record_flush(k4a_record_t recording_handle);
		self.k4a_record_flush = recorddll.k4a_record_flush
		self.k4a_record_flush.restype = k4a_result_t
		self.k4a_record_flush.argtypes = (k4a_record_t,)

		# K4ARECORD_EXPORT void k4a_record_close(k4a_record_t recording_handle);
		self.k4a_record_close = recorddll.k4a_record_close
		self.k4a_record_close.restype = None
		self.k4a_record_close.argtypes = (k4a_record_t,)


					###########################
					###    Playback         ###
					###########################

		
		# K4ARECORD_EXPORT k4a_result_t k4a_playback_open(const char *path, k4a_playback_t *playback_handle);
		self.k4a_playback_open = recorddll.k4a_playback_open
		self.k4a_playback_open.restype = k4a_result_t
		self.k4a_playback_open.argtypes = (ctypes.POINTER(ctypes.c_char), \
										   ctypes.POINTER(k4a_playback_t),)

		# K4ARECORD_EXPORT void k4a_playback_close(k4a_playback_t playback_handle);
		self.k4a_playback_close = recorddll.k4a_playback_close
		self.k4a_playback_close.restype = None
		self.k4a_playback_close.argtypes = (k4a_playback_t,)

		"""
		K4ARECORD_EXPORT k4a_stream_result_t k4a_playback_get_next_capture(k4a_playback_t playback_handle,
																	   k4a_capture_t *capture_handle);
		"""
		self.k4a_playback_get_next_capture = recorddll.k4a_playback_get_next_capture
		self.k4a_playback_get_next_capture.restype = k4a_stream_result_t
		self.k4a_playback_get_next_capture.argtypes = (k4a_playback_t, \
													   ctypes.POINTER(k4a_capture_t),)


		"""
		K4ARECORD_EXPORT k4a_stream_result_t k4a_playback_get_previous_capture(k4a_playback_t playback_handle,
																		   k4a_capture_t *capture_handle);
		"""
		self.k4a_playback_get_previous_capture = recorddll.k4a_playback_get_next_capture
		self.k4a_playback_get_previous_capture.restype = k4a_stream_result_t
		self.k4a_playback_get_previous_capture.argtypes = (k4a_playback_t, \
													   ctypes.POINTER(k4a_capture_t),)


		"""
		K4ARECORD_EXPORT k4a_result_t k4a_playback_get_calibration(k4a_playback_t playback_handle,
																   k4a_calibration_t *calibration);
		"""
		self.k4a_playback_get_calibration = recorddll.k4a_playback_get_calibration
		self.k4a_playback_get_calibration.restype = k4a_result_t
		self.k4a_playback_get_calibration.argtypes = (k4a_playback_t, \
													ctypes.POINTER(k4a_calibration_t), \
													)



def VERIFY(result, error):
	if result != K4A_RESULT_SUCCEEDED:
		print(error)
		traceback.print_stack()
		sys.exit(1)

