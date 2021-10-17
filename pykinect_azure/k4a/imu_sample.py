from pykinect_azure.utils import getdict

class ImuSample:

	def __init__(self, imu_sample_struct):

		self._struct = imu_sample_struct
		self.parse_data()

	def __del__(self):

		self.reset()

	def is_valid(self):
		return self._struct

	def struct(self):
		return self._struct

	def reset(self):
		if self.is_valid():
			self._struct = None

	def parse_data(self):
		self.imu_sample_dict = getdict(self._struct)

		# Convert the acc and gyro dicts to numpy array
		self.imu_sample_dict["acc_sample"] = self.imu_sample_dict["acc_sample"]["v"]
		self.imu_sample_dict["gyro_sample"] = self.imu_sample_dict["gyro_sample"]["v"]

	@property
	def temp(self):
		return self.get_temp()
		
	@property
	def acc(self):
		return self.get_acc()

	@property
	def acc_time(self):
		return self.get_acc_time()

	@property
	def gyro(self):
		return self.get_gyro()

	@property
	def gyro_time(self):
		return self.get_gyro_time()

	def get_temp(self):
		return self.imu_sample_dict["temperature"]

	def get_acc(self):
		return self.imu_sample_dict["acc_sample"]

	def get_acc_time(self):
		return self.imu_sample_dict["acc_timestamp_usec"]

	def get_gyro(self):
		return self.imu_sample_dict["gyro_sample"]

	def get_gyro_time(self):
		return self.imu_sample_dict["gyro_timestamp_usec"]

	def get_sample(self):
		return self.imu_sample_dict


