from _k4atypes import k4a_float3_t, k4a_float2_t, k4a_calibration_t, k4a_capture_t, k4a_image_t
import ctypes
import numpy as np

# K4A_DECLARE_HANDLE(k4abt_tracker_t);
class _handle_k4abt_tracker_t(ctypes.Structure):
     _fields_= [
        ("_rsvd", ctypes.c_size_t),
    ]
k4abt_tracker_t = ctypes.POINTER(_handle_k4abt_tracker_t)

# K4A_DECLARE_HANDLE(k4abt_frame_t);
class _handle_k4abt_frame_t(ctypes.Structure):
     _fields_= [
        ("_rsvd", ctypes.c_size_t),
    ]
k4abt_frame_t = ctypes.POINTER(_handle_k4abt_frame_t)

k4abt_result_t = ctypes.c_int
K4ABT_RESULT_SUCCEEDED = 0
K4ABT_RESULT_FAILED = 1

#class k4abt_joint_id_t(CtypeIntEnum):
K4ABT_JOINT_PELVIS = 0
K4ABT_JOINT_SPINE_NAVEL = 1
K4ABT_JOINT_SPINE_CHEST = 2
K4ABT_JOINT_NECK = 3
K4ABT_JOINT_CLAVICLE_LEFT = 4
K4ABT_JOINT_SHOULDER_LEFT = 5
K4ABT_JOINT_ELBOW_LEFT = 6
K4ABT_JOINT_WRIST_LEFT = 7
K4ABT_JOINT_HAND_LEFT = 8
K4ABT_JOINT_HANDTIP_LEFT = 9
K4ABT_JOINT_THUMB_LEFT = 10
K4ABT_JOINT_CLAVICLE_RIGHT = 11
K4ABT_JOINT_SHOULDER_RIGHT = 12
K4ABT_JOINT_ELBOW_RIGHT = 13
K4ABT_JOINT_WRIST_RIGHT = 14
K4ABT_JOINT_HAND_RIGHT = 15
K4ABT_JOINT_HANDTIP_RIGHT = 16
K4ABT_JOINT_THUMB_RIGHT = 17
K4ABT_JOINT_HIP_LEFT = 18
K4ABT_JOINT_KNEE_LEFT = 19
K4ABT_JOINT_ANKLE_LEFT = 20
K4ABT_JOINT_FOOT_LEFT = 21
K4ABT_JOINT_HIP_RIGHT = 22
K4ABT_JOINT_KNEE_RIGHT = 23
K4ABT_JOINT_ANKLE_RIGHT = 24
K4ABT_JOINT_FOOT_RIGHT = 25
K4ABT_JOINT_HEAD = 26
K4ABT_JOINT_NOSE = 27
K4ABT_JOINT_EYE_LEFT = 28
K4ABT_JOINT_EAR_LEFT = 29
K4ABT_JOINT_EYE_RIGHT = 30
K4ABT_JOINT_EAR_RIGHT = 31
K4ABT_JOINT_COUNT = 32

K4ABT_SEGMENT_PAIRS = [[1, 0], 
                       [2, 1], 
                       [3, 2], 
                       [4, 2], 
                       [5, 4], 
                       [6, 5], 
                       [7, 6], 
                       [8, 7], 
                       [9, 8],
                       [10, 7], 
                       [11, 2], 
                       [12, 11], 
                       [13, 12], 
                       [14, 13], 
                       [15, 14], 
                       [16, 15], 
                       [17, 14], 
                       [18, 0], 
                       [19, 18],
                       [20, 19], 
                       [21, 20], 
                       [22, 0], 
                       [23, 22], 
                       [24, 23], 
                       [25, 24], 
                       [26, 3], 
                       [27, 26],
                       [28, 26], 
                       [29, 26], 
                       [30, 26], 
                       [31, 26]]

#class k4abt_sensor_orientation_t(CtypeIntEnum):
K4ABT_SENSOR_ORIENTATION_DEFAULT = 0
K4ABT_SENSOR_ORIENTATION_CLOCKWISE90 = 1
K4ABT_SENSOR_ORIENTATION_COUNTERCLOCKWISE90 = 2
K4ABT_SENSOR_ORIENTATION_FLIP180 = 3

#class k4abt_tracker_processing_mode_t(CtypeIntEnum):
K4ABT_TRACKER_PROCESSING_MODE_GPU = 0
K4ABT_TRACKER_PROCESSING_MODE_CPU = 1
K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA = 2     
K4ABT_TRACKER_PROCESSING_MODE_GPU_TENSORRT = 3
K4ABT_TRACKER_PROCESSING_MODE_GPU_DIRECTML = 4

class _k4abt_tracker_configuration_t(ctypes.Structure):
    _fields_= [
        ("sensor_orientation", ctypes.c_int),
        ("processing_mode", ctypes.c_int),
        ("gpu_device_id", ctypes.c_int32),
        ("model_path", ctypes.c_char_p),
    ]
k4abt_tracker_configuration_t = _k4abt_tracker_configuration_t

class _wxyz(ctypes.Structure):
    _fields_= [
        ("w", ctypes.c_float),
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]

class k4a_quaternion_t(ctypes.Union):
   _fields_= [
        ("wxyz", _wxyz),
        ("v", ctypes.c_float * 4)
    ]

#class k4abt_joint_confidence_level_t(CtypeIntEnum):
K4ABT_JOINT_CONFIDENCE_NONE = 0
K4ABT_JOINT_CONFIDENCE_LOW = 1
K4ABT_JOINT_CONFIDENCE_MEDIUM = 2
K4ABT_JOINT_CONFIDENCE_HIGH = 3
K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT = 4


class _k4abt_joint_t(ctypes.Structure):
    _fields_= [
        ("position", k4a_float3_t),
        ("orientation", k4a_quaternion_t),
        ("confidence_level", ctypes.c_int),
    ]
k4abt_joint_t = _k4abt_joint_t

class k4abt_skeleton_t(ctypes.Structure):
    _fields_= [
        ("joints", _k4abt_joint_t * K4ABT_JOINT_COUNT),
    ]

class k4abt_body_t(ctypes.Structure):
    _fields_= [
        ("id", ctypes.c_uint32),
        ("skeleton", k4abt_skeleton_t),
    ]

class _k4abt_joint2D_t(ctypes.Structure):
    _fields_= [
        ("position", k4a_float2_t),
        ("confidence_level", ctypes.c_int),
    ]
k4abt_joint2D_t = _k4abt_joint2D_t

class k4abt_skeleton2D_t(ctypes.Structure):
    _fields_= [
        ("joints2D", _k4abt_joint2D_t * K4ABT_JOINT_COUNT),
    ]

class k4abt_body2D_t(ctypes.Structure):
    _fields_= [
        ("id", ctypes.c_uint32),
        ("skeleton", k4abt_skeleton2D_t),
    ]


K4ABT_BODY_INDEX_MAP_BACKGROUND = 255
K4ABT_INVALID_BODY_ID = 0xFFFFFFFF
K4ABT_DEFAULT_TRACKER_SMOOTHING_FACTOR = 0.0

K4ABT_DEFAULT_MODEL = 0
K4ABT_LITE_MODEL = 1

# TODO(Andoryuuta): Not sure if a single instance of the default config like this will work, might need a creation function.
K4ABT_TRACKER_CONFIG_DEFAULT = k4abt_tracker_configuration_t()
K4ABT_TRACKER_CONFIG_DEFAULT.sensor_orientation = K4ABT_SENSOR_ORIENTATION_DEFAULT
K4ABT_TRACKER_CONFIG_DEFAULT.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_GPU
K4ABT_TRACKER_CONFIG_DEFAULT.gpu_device_id = 0

body_colors = np.ones((256,3), dtype=np.uint8)*K4ABT_BODY_INDEX_MAP_BACKGROUND
body_colors[:7,:] = np.array([[202, 183, 42], [42, 61, 202], [42, 202, 183], [202, 42,61], [183, 42, 202], [42, 202, 61], [141, 202, 42]]) 