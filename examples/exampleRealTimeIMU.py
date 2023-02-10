import numpy as np
import matplotlib.pyplot as plt

import pykinect_azure as pykinect

def handle_close(evt):
	global keep_running
	keep_running = False

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_OFF
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	acc_mat = np.empty((0,3), np.float32)
	gyro_mat = np.empty((0,3), np.float32)
	time_mat = np.empty((0,1), int)	

	fig = plt.figure()	
	fig.canvas.mpl_connect('close_event', handle_close)
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)
	keep_running = True

	while keep_running:

		# Get imu sample
		imu_sample = device.update_imu()

		# Extract the sensor data
		sample_time = imu_sample.acc_time
		acc_sample = imu_sample.acc
		gyro_sample = imu_sample.gyro

		# print(sample_time, acc_sample, gyro_sample)

		# Add current sample data to the matrices
		acc_mat = np.vstack((acc_mat, acc_sample))
		gyro_mat = np.vstack((gyro_mat, gyro_sample))
		time_mat = np.vstack((time_mat,sample_time))

		ax1.plot(time_mat/1e6,acc_mat)
		ax2.plot(time_mat/1e6,gyro_mat)
		plt.pause(0.01)
		ax1.cla()
		ax2.cla()


	




