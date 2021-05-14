import ctypes
import sys
from _k4abtTypes import *
import traceback

_library_handle = None

class k4abt:

	def __init__(self):

		dll = _library_handle
		
		"""
		K4ABT_EXPORT k4a_result_t k4abt_tracker_create(const k4a_calibration_t* sensor_calibration,
                                                k4abt_tracker_configuration_t config,
                                                k4abt_tracker_t* tracker_handle);
        """
		self.k4abt_tracker_create = dll.k4abt_tracker_create
		self.k4abt_tracker_create.restype=ctypes.c_int
		self.k4abt_tracker_create.argtypes=(ctypes.POINTER(k4a_calibration_t), k4abt_tracker_configuration_t, ctypes.POINTER(k4abt_tracker_t))

		# K4ABT_EXPORT void k4abt_tracker_destroy(k4abt_tracker_t tracker_handle);
		self.k4abt_tracker_destroy = dll.k4abt_tracker_destroy
		self.k4abt_tracker_destroy.argtypes=(k4abt_tracker_t,)

		# K4ABT_EXPORT void k4abt_tracker_set_temporal_smoothing(k4abt_tracker_t tracker_handle, float smoothing_factor);
		self.k4abt_tracker_set_temporal_smoothing = dll.k4abt_tracker_set_temporal_smoothing
		self.k4abt_tracker_set_temporal_smoothing.argtypes=(k4abt_tracker_t, ctypes.c_float)

		"""
		K4ABT_EXPORT k4a_wait_result_t k4abt_tracker_enqueue_capture(k4abt_tracker_t tracker_handle,
                                                              k4a_capture_t sensor_capture_handle,
                                                              int32_t timeout_in_ms);
        """
		self.k4abt_tracker_enqueue_capture = dll.k4abt_tracker_enqueue_capture
		self.k4abt_tracker_enqueue_capture.restype=ctypes.c_int
		self.k4abt_tracker_enqueue_capture.argtypes=(k4abt_tracker_t, k4a_capture_t, ctypes.c_int32)

		"""
 		K4ABT_EXPORT k4a_wait_result_t k4abt_tracker_pop_result(k4abt_tracker_t tracker_handle,
		                                                         k4abt_frame_t* body_frame_handle,
		                                                         int32_t timeout_in_ms);

		"""
		self.k4abt_tracker_pop_result = dll.k4abt_tracker_pop_result
		self.k4abt_tracker_pop_result.restype=ctypes.c_int
		self.k4abt_tracker_pop_result.argtypes=(k4abt_tracker_t, ctypes.POINTER(k4abt_frame_t), ctypes.c_int32)

		# K4ABT_EXPORT void k4abt_tracker_shutdown(k4abt_tracker_t tracker_handle);
		self.k4abt_tracker_shutdown = dll.k4abt_tracker_shutdown
		self.k4abt_tracker_shutdown.argtypes=(k4abt_tracker_t,)

		# K4ABT_EXPORT void k4abt_frame_release(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_release = dll.k4abt_frame_release
		self.k4abt_frame_release.argtypes=(k4abt_frame_t,)

		# K4ABT_EXPORT void k4abt_frame_reference(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_reference = dll.k4abt_frame_reference
		self.k4abt_frame_reference.argtypes=(k4abt_frame_t,)

		# K4ABT_EXPORT uint32_t k4abt_frame_get_num_bodies(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_get_num_bodies = dll.k4abt_frame_get_num_bodies
		self.k4abt_frame_get_num_bodies.restype=ctypes.c_uint32
		self.k4abt_frame_get_num_bodies.argtypes=(k4abt_frame_t,)

		# K4ABT_EXPORT k4a_result_t k4abt_frame_get_body_skeleton(k4abt_frame_t body_frame_handle, uint32_t index, k4abt_skeleton_t* skeleton);
		self.k4abt_frame_get_body_skeleton = dll.k4abt_frame_get_body_skeleton
		self.k4abt_frame_get_body_skeleton.restype=ctypes.c_int
		self.k4abt_frame_get_body_skeleton.argtypes=(k4abt_frame_t, ctypes.c_uint32, ctypes.POINTER(k4abt_skeleton_t))

		# K4ABT_EXPORT uint32_t k4abt_frame_get_body_id(k4abt_frame_t body_frame_handle, uint32_t index);
		self.k4abt_frame_get_body_id = dll.k4abt_frame_get_body_id
		self.k4abt_frame_get_body_id.restype=ctypes.c_uint32
		self.k4abt_frame_get_body_id.argtypes=(k4abt_frame_t, ctypes.c_uint32)

		# K4ABT_EXPORT uint64_t k4abt_frame_get_device_timestamp_usec(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_get_device_timestamp_usec = dll.k4abt_frame_get_device_timestamp_usec
		self.k4abt_frame_get_device_timestamp_usec.restype=ctypes.c_uint64
		self.k4abt_frame_get_device_timestamp_usec.argtypes=(k4abt_frame_t,)

		#  K4ABT_EXPORT k4a_image_t k4abt_frame_get_body_index_map(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_get_body_index_map = dll.k4abt_frame_get_body_index_map
		self.k4abt_frame_get_body_index_map.restype=k4a_image_t
		self.k4abt_frame_get_body_index_map.argtypes=(k4abt_frame_t,)

		# K4ABT_EXPORT k4a_capture_t k4abt_frame_get_capture(k4abt_frame_t body_frame_handle);
		self.k4abt_frame_get_capture = dll.k4abt_frame_get_capture
		self.k4abt_frame_get_capture.restype=k4a_capture_t
		self.k4abt_frame_get_capture.argtypes=(k4abt_frame_t,)

	@staticmethod
	def setup_library(modulePath):

		global _library_handle

		try: 
			_library_handle = ctypes.CDLL(modulePath)

		except Exception as e:

			if e.winerror == 193:
				print("Failed to load library. \n\nChange the module path to the 32 bit version.")
				sys.exit(1)

			print(e, "\n\nFailed to load Windows library. Trying to load Linux library...\n")

			try:
				_library_handle = ctypes.CDLL('k4abt.so')
			except Exception as ee:
				print("Failed to load library", ee)
				sys.exit(1)

def VERIFY(result, error):
	if result != K4ABT_RESULT_SUCCEEDED:
		print(error)
		traceback.print_stack()
		sys.exit(1)

