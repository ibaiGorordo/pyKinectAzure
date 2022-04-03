import numpy as np
import platform
import sys


def get_k4a_module_path():

    # Check if running in Jetson Nano or similar ARM chips
    if platform.machine().lower() == 'aarch64':
        return r'/usr/lib/aarch64-linux-gnu/libk4a.so'

    # For non-Arm chips, first check if it is running linux
    if platform.system().lower() == 'linux':
        return r'/usr/lib/x86_64-linux-gnu/libk4a.so'

    # In Windows check the architecture
    if platform.machine().lower() == 'amd64':
        return 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

    # Otherwise return the x86 Windows version
    return 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\x86\\release\\bin\\k4a.dll'

def get_k4abt_module_path():

    # Check if running in Jetson Nano or similar ARM chips
    if platform.machine().lower() == 'aarch64':
        print("Kinect Body Tracking is not implemented yet in ARM. Check https://feedback.azure.com/forums/920053 for more info.")
        sys.exit(1)

    # For non-Arm chips, first check if it is running linux
    if platform.system().lower() == 'linux':
        return 'libk4abt.so'

    # Otherwise return the Windows version
    return 'C:\\Program Files\\Azure Kinect Body Tracking SDK\\sdk\\windows-desktop\\amd64\\release\\bin\\k4abt.dll'

def get_k4arecord_module_path(modulePath):
    return modulePath.replace('k4a', 'k4arecord')

def get_k4abt_lite_model_path():

    # Check if it is a Linux system
    if platform.system().lower() == 'linux':
        return None

    # Return the Windows version
    return 'C:/Program Files/Azure Kinect Body Tracking SDK/sdk/windows-desktop/amd64/release/bin/dnn_model_2_0_lite_op11.onnx'.encode('utf-8')

def getdict(struct):
	result = {}
	for field, _ in struct._fields_:
		value = getattr(struct, field)
		# if the type is not a primitive and it evaluates to False ...
		if (type(value) not in [int, float, bool]) and not bool(value):
			# it's a null pointer
			value = None
		elif hasattr(value, "_length_") and hasattr(value, "_type_"):
			# Probably an array
			value = np.array(list(value))
		elif hasattr(value, "_fields_"):
			# Probably another struct
			value = getdict(value)
		result[field] = value
	return result
