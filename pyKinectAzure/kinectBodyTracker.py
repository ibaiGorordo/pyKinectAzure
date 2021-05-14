import _k4a
import _k4abt
import numpy as np
import cv2
import sys
import ctypes
from ctypes import cdll
from config import config
import postProcessing
import platform

class kinectBodyTracker:

	def __init__(self, modulePath, sensor_calibration, modelType):

		_k4abt.k4abt.setup_library(modulePath)
		self.k4abt = _k4abt.k4abt()

		try:
			cdll.LoadLibrary("C:/Program Files/Azure Kinect Body Tracking SDK/tools/directml.dll")
		except Exception as e:
			_k4abt.K4ABT_TRACKER_CONFIG_DEFAULT.processing_mode  = _k4abt.K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA

		self.tracker_handle = _k4abt.k4abt_tracker_t()	
		if modelType == 1:
			try: 
				_k4abt.K4ABT_TRACKER_CONFIG_DEFAULT.model_path = "C:/Program Files/Azure Kinect Body Tracking SDK/sdk/windows-desktop/amd64/release/bin/dnn_model_2_0_lite_op11.onnx".encode('utf-8')
			except Exception as e:
				print("Failed to find lite model. Check that you are using Body Tracker version 1.1.0\n")
				print("Switching to the original body tracking model\n\n\n")
			
		self.tracker_config = _k4abt.K4ABT_TRACKER_CONFIG_DEFAULT
		self.body_frame_handle = _k4abt.k4abt_frame_t()
		self.segmented_body_img = _k4a.k4a_image_t()
		self.capture_handle = _k4a.k4a_capture_t()
		self.sensor_calibration = sensor_calibration

		self.tracker_running = False
		self.bodiesNow = []

		self.initializeTracker()

	def detectBodies(self):

		self.bodiesNow = []

		# Get the next available body frame.
		self.pop_result()

		# Get the semantic body image 
		self.get_body_index_map()

		# Get the number of people in the frame
		num_bodies = self.get_num_bodies()

		# Extract the skeleton of each person
		if num_bodies:
			for bodyIdx in range(num_bodies):
				body = _k4abt.k4abt_body_t()
				body.skeleton = self.get_body_skeleton(bodyIdx);
				body.id = self.get_body_id(bodyIdx);

				self.bodiesNow.append(body)

	def printBodyPosition(self, body):
		print(f"BodyId: {body.id}", \
			  f"X: {body.skeleton.joints[_k4abt.K4ABT_JOINT_SPINE_NAVEL].position.v[0]:.2f} mm", \
			  f"Y: {body.skeleton.joints[_k4abt.K4ABT_JOINT_SPINE_NAVEL].position.v[1]:.2f} mm", \
			  f"Z: {body.skeleton.joints[_k4abt.K4ABT_JOINT_SPINE_NAVEL].position.v[2]:.2f} mm") 

	def draw2DSkeleton(self, skeleton2D, bodyId, image):
		color = _k4abt.body_colors
		for joint in skeleton2D.joints2D:
			image = cv2.circle(image, (int(joint.position.v[0]), int(joint.position.v[1])), 3, (255,0,0), 3)

		for segmentId in range(len(_k4abt.K4ABT_SEGMENT_PAIRS)):
			point1 = skeleton2D.joints2D[_k4abt.K4ABT_SEGMENT_PAIRS[segmentId][0]].position.v
			point2 = skeleton2D.joints2D[_k4abt.K4ABT_SEGMENT_PAIRS[segmentId][1]].position.v
			image = cv2.line(
                image, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])),
                (255,0,0), 2
            )

		return image

	def initializeTracker(self):
		"""Initialize the body tracker

		Parameters:
		k4a_calibration_t calibration: Camera calibration for capture processing
		k4abt_tracker_configuration_t config: Cofiguration for the body tracker
		k4abt_tracker_t* tracker_handle: handle of the body tracker
			
		Returns:
		None
		
		Remarks:
		If successful, k4abt_tracker_create() will return a body tracker handle in the tracker parameter. This handle grants
		* access to the body tracker and may be used in the other k4abt API calls.

		When done with body tracking, close the handle with k4abt_tracker_destroy().
		"""
		_k4abt.VERIFY(self.k4abt.k4abt_tracker_create(self.sensor_calibration, self.tracker_config, self.tracker_handle), "Body tracker initialization failed!")
		self.tracker_running = True

	def destroyTracker(self):
		""" Releases a body tracker handle.

		Parameters:
		k4abt_tracker_t tracker_handle: tracker handle to be released
			
		Returns:
		None
		
		Remarks:
		 Once released, the tracker_handle is no longer valid.
		"""
		self.k4abt.k4abt_tracker_destroy(self.tracker_handle)
		self.tracker_running = False

	def shutdown(self):
		""" Shutdown the tracker so that no further capture can be added to the input queue.

		Parameters:
		k4abt_tracker_t tracker_handle: tracker handle to be released
			
		Returns:
		None
		
		Remarks:
		Once the tracker is shutdown, k4abt_tracker_enqueue_capture() API will always immediately return failure.

		If there are remaining catpures in the tracker queue after the tracker is shutdown, k4abt_tracker_pop_result() can
		still return successfully. Once the tracker queue is empty, the k4abt_tracker_pop_result() call will always immediately
		return failure.
		"""
		self.k4abt.k4abt_tracker_shutdown(self.tracker_handle)
		self.tracker_running = False

	def set_temporal_smoothing(self, smoothing_factor):
		""" Control the temporal smoothing across frames.

		Parameters:
		k4abt_tracker_t tracker_handle: Handle obtained by k4abt_tracker_create().
		float smoothing_factor: Set between 0 for no smoothing and 1 for full smoothing. Less smoothing will increase the responsiveness of the
								detected skeletons but will cause more positional and orientational jitters.
			
		Returns:
		None
		
		Remarks:
		The default smoothness value is defined as K4ABT_DEFAULT_TRACKER_SMOOTHING_FACTOR.
		"""
		self.k4abt.k4abt_tracker_set_temporal_smoothing(self.tracker_handle, smoothing_factor)

	def enqueue_capture(self, capture_handle, timeout_in_ms=_k4a.K4A_WAIT_INFINITE):
		"""Add a k4a sensor capture to the tracker input queue to generate its body tracking result asynchronously.

		Parameters:h
		k4a_capture_t sensor_capture_handle: Handle to a sensor capture returned by k4a_device_get_capture() from k4a SDK.
		timeout_in_ms (int):Specifies the time in milliseconds the function should block waiting for the capture. If set to 0, the function will
							return without blocking. Passing a value of #K4A_WAIT_INFINITE will block indefinitely until data is available, the
							device is disconnected, or another error occurs.

		Returns:
		None

		Remarks:
		Add a k4a capture to the tracker input queue so that it can be processed asynchronously to generate the body tracking
		result. The processed results will be added to an output queue maintained by k4abt_tracker_t instance. Call
		k4abt_tracker_pop_result to get the result and pop it from the output queue.
		If the input queue or output queue is full, this function will block up until the timeout is reached.
		Once body_frame data is read, the user must call k4abt_frame_release() to return the allocated memory to the SDK

		Upon successfully insert a sensor capture to the input queue this function will return success.
		"""
		_k4abt.VERIFY(self.k4abt.k4abt_tracker_enqueue_capture(self.tracker_handle, capture_handle, timeout_in_ms), "Body tracker capture enqueue failed!")

	def pop_result(self, timeout_in_ms=_k4a.K4A_WAIT_INFINITE):
		"""Gets the next available body frame.

		Parameters:
		k4abt_frame_t* body_frame_handle: If successful this contains a handle to a body frame object.
		timeout_in_ms (int):Specifies the time in milliseconds the function should block waiting for the capture. If set to 0, the function will
							return without blocking. Passing a value of #K4A_WAIT_INFINITE will block indefinitely until data is available, the
							device is disconnected, or another error occurs.

		Returns:
		None

		Remarks:
		Retrieves the next available body frame result and pop it from the output queue in the k4abt_tracker_t. If a new body
		frame is not currently available, this function will block up until the timeout is reached. The SDK will buffer at
		least three body frames worth of data before stopping new capture being queued by k4abt_tracker_enqueue_capture.
		Once body_frame data is read, the user must call k4abt_frame_release() to return the allocated memory to the SDK.

		Upon successfully reads a body frame this function will return success.
		"""
		if self.tracker_running:
			_k4abt.VERIFY(self.k4abt.k4abt_tracker_pop_result(self.tracker_handle, self.body_frame_handle, timeout_in_ms), "Body tracker get body frame failed!")
	
	def release_frame(self):
		"""Release a body frame back to the SDK

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object to return to SDK.
		
		Returns:
		None

		Remarks:
		Called when the user is finished using the body frame.
		"""
		self.k4abt.k4abt_frame_release(self.body_frame_handle)

	def add_reference_to_frame(self):
		"""Add a reference to a body frame.

		Parameters:
		k4abt_frame_t* body_frame_handle: Body frame to add a reference to.
		
		Returns:
		None

		Remarks:
		Call this function to add an additional reference to a body frame. This reference must be removed with
		k4abt_frame_release().
		"""
		self.k4abt.k4abt_frame_reference(self.body_frame_handle)

	def get_num_bodies(self):
		"""Get the number of people from the k4abt_frame_t

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		
		Returns:
		uint32_t number_of_bodies: Returns the number of detected bodies. 0 if the function fails.

		Remarks:
		Called when the user has received a body frame handle and wants to access the data contained in it.
		"""
		return self.k4abt.k4abt_frame_get_num_bodies(self.body_frame_handle)

	def get_body_skeleton(self, index=0):
		"""Get the joint information for a particular person index from the k4abt_frame_t

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		uint32_t index: The index of the body of which the joint information is queried.
		
		Returns:
		k4abt_skeleton_t* skeleton: If successful this contains the body skeleton information.

		Remarks:
		Called when the user has received a body frame handle and wants to access the data contained in it.
		"""
		skeleton = _k4abt.k4abt_skeleton_t()

		_k4abt.VERIFY(self.k4abt.k4abt_frame_get_body_skeleton(self.body_frame_handle, index, skeleton), "Body tracker get body skeleton failed!")

		return skeleton

	def get_body_id(self, index=0):
		"""Get the joint information for a particular person index from the k4abt_frame_t

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		uint32_t index: The index of the body of which the body id information is queried.
		
		Returns:
		uint32_t body_id: Returns the body id. All failures will return K4ABT_INVALID_BODY_ID.

		Remarks:
		Called when the user has received a body frame handle and wants to access the id of the body given a
		particular index.
		"""
		return self.k4abt.k4abt_frame_get_body_id(self.body_frame_handle, index)

	def get_device_timestamp_usec(self):
		""" Get the body frame's device timestamp in microseconds

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		
		Returns:
		uint64_t timestamp: Returns the timestamp of the body frame. If the body_frame_handle is invalid this function will return 0.

		Remarks:
		Called when the user has received a body frame handle and wants to access the data contained in it.
		"""
		return self.k4abt.k4abt_frame_get_device_timestamp_usec(self.body_frame_handle)

	def get_body_index_map(self):
		""" Get the body index map from k4abt_frame_t

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		
		Returns:
		k4a_image_t segmented_body_img: Call this function to access the body index map image.

		Remarks:
		Body Index map is the body instance segmentation map. Each pixel maps to the corresponding pixel in the
		depth image or the ir image. The value for each pixel represents which body the pixel belongs to. It can be either
		background (value K4ABT_BODY_INDEX_MAP_BACKGROUND) or the index of a detected k4abt_body_t.
		"""
		self.segmented_body_img = self.k4abt.k4abt_frame_get_body_index_map(self.body_frame_handle)

	def get_frame_capture(self):
		""" Get the original capture that is used to calculate the k4abt_frame_t

		Parameters:
		k4abt_frame_t* body_frame_handle: Handle to a body frame object returned by k4abt_tracker_pop_result function.
		
		Returns:
		k4a_capture_t capture_handle: Call this function to access the original k4a_capture_t

		Remarks:
		Called when the user has received a body frame handle and wants to access the data contained in it.
		"""
		self.capture_handle = self.k4abt.k4abt_frame_get_capture(self.body_frame_handle)
