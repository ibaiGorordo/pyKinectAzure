from pykinect_azure.k4a import _k4a

class Configuration:

	def __init__(self, configuration_handle=None):

		if configuration_handle:
			self._handle = configuration_handle
		else:
			self._handle = self.create()

	def handle(self):

		return self._handle

	def __setattr__(self, name, value):
		"""Run on change function when configuration parameters are changed"""

		if name == "_handle":
			self.__dict__[name] = value
		else:
			self._handle.__dict__[name] = value

	def __getattr__(self, name):
		"""Pass the handle parameter, when asked"""

		if name == "_handle":
			return self.__dict__[name]
		else:
			return self._handle.__dict__[name]

	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = (
			"Device configuration: \n"
			f"\tcolor_format: {self._handle.color_format} \n\t(0:JPG, 1:NV12, 2:YUY2, 3:BGRA32)\n\n"
			f"\tcolor_resolution: {self._handle.color_resolution} \n\t(0:OFF, 1:720p, 2:1080p, 3:1440p, 4:1536p, 5:2160p, 6:3072p)\n\n"
			f"\tdepth_mode: {self._handle.depth_mode} \n\t(0:OFF, 1:NFOV_2X2BINNED, 2:NFOV_UNBINNED,3:WFOV_2X2BINNED, 4:WFOV_UNBINNED, 5:Passive IR)\n\n"
			f"\tcamera_fps: {self._handle.camera_fps} \n\t(0:5 FPS, 1:15 FPS, 2:30 FPS)\n\n"
			f"\tsynchronized_images_only: {self._handle.synchronized_images_only} \n\t(True of False). Drop images if the color and depth are not synchronized\n\n"
			f"\tdepth_delay_off_color_usec: {self._handle.depth_delay_off_color_usec} us. \n\tDelay between the color image and the depth image\n\n"
			f"\twired_sync_mode: {self._handle.wired_sync_mode}\n\t(0:Standalone mode, 1:Master mode, 2:Subordinate mode)\n\n"
			f"\tsubordinate_delay_off_master_usec: {self._handle.subordinate_delay_off_master_usec} us.\n\tThe external synchronization timing.\n\n"
			f"\tdisable_streaming_indicator: {self._handle.disable_streaming_indicator} \n\t(True or False). Streaming indicator automatically turns on when the color or depth camera's are in use.\n\n"
			)
		return message

	@staticmethod
	def create():

		return _k4a.k4a_device_configuration_t(_k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32, \
											_k4a.K4A_COLOR_RESOLUTION_720P,\
											_k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED,\
											_k4a.K4A_FRAMES_PER_SECOND_30,\
											False,\
											0,\
											_k4a.K4A_WIRED_SYNC_MODE_STANDALONE,\
											0,\
											False)

default_configuration = Configuration()