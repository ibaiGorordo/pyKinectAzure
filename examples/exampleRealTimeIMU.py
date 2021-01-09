import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2
import matplotlib.pyplot as plt

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll' 
# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

def handle_close(evt):
	global keep_running
	keep_running = False
    

if __name__ == "__main__":

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Start cameras using modified configuration
	pyK4A.device_start_cameras()

	# Start IMU 
	pyK4A.device_start_imu()

	acc_mat = np.empty((0,3), np.float32)
	gyro_mat = np.empty((0,3), np.float32)
	time_mat = np.empty((0,1), int)	

	fig = plt.figure()	
	fig.canvas.mpl_connect('close_event', handle_close)
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)
	keep_running = True
	try:
		while keep_running:
			# Get IMU sample
			imu_results = pyK4A.get_imu_sample()

			# Add current sample data to the matrices
			acc_mat = np.vstack((acc_mat, imu_results.acc_sample))
			gyro_mat = np.vstack((gyro_mat, imu_results.gyro_sample))
			time_mat = np.vstack((time_mat,imu_results.acc_timestamp_usec))

			ax1.plot(time_mat/1e6,acc_mat)
			ax2.plot(time_mat/1e6,gyro_mat)
			plt.pause(0.01)
			ax1.cla()
			ax2.cla()

	except KeyboardInterrupt:
		pass
		
	
	pyK4A.device_stop_imu()
	pyK4A.device_stop_cameras()
	pyK4A.device_close()


