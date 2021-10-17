from pykinect_azure.k4a import _k4a

class RecordConfiguration:

	def __init__(self, configuration_handle=None):

		self._handle = configuration_handle

	def handle(self):

		return self._handle

	def __getattr__(self, name):
		"""Pass the handle parameter, when asked"""

		if name == "_handle":
			return self.__dict__[name]
		else:
			return self._handle.__dict__[name]

	def __str__(self):
		"""Print the current settings and a short explanation"""
		message = (
			"Record configuration: \n"
			f"\tcolor_format: {self._handle.color_format} \n\t(0:JPG, 1:NV12, 2:YUY2, 3:BGRA32)\n\n"
			f"\tcolor_resolution: {self._handle.color_resolution} \n\t(0:OFF, 1:720p, 2:1080p, 3:1440p, 4:1536p, 5:2160p, 6:3072p)\n\n"
			f"\tdepth_mode: {self._handle.depth_mode} \n\t(0:OFF, 1:NFOV_2X2BINNED, 2:NFOV_UNBINNED,3:WFOV_2X2BINNED, 4:WFOV_UNBINNED, 5:Passive IR)\n\n"
			f"\tcamera_fps: {self._handle.camera_fps} \n\t(0:5 FPS, 1:15 FPS, 2:30 FPS)\n\n"
			f"\tcolor_track_enabled: {self._handle.color_track_enabled} \n\t(True of False). If Color camera images exist\n\n"
			f"\tdepth_track_enabled: {self._handle.depth_track_enabled} \n\t(True of False). If Depth camera images exist\n\n"
			f"\tir_track_enabled: {self._handle.ir_track_enabled} \n\t(True of False). If IR camera images exist\n\n"
			f"\timu_track_enabled: {self._handle.imu_track_enabled} \n\t(True of False). If IMU samples exist\n\n"
			f"\tdepth_delay_off_color_usec: {self._handle.depth_delay_off_color_usec} us. \n\tDelay between the color image and the depth image\n\n"
			f"\twired_sync_mode: {self._handle.wired_sync_mode}\n\t(0:Standalone mode, 1:Master mode, 2:Subordinate mode)\n\n"
			f"\tsubordinate_delay_off_master_usec: {self._handle.subordinate_delay_off_master_usec} us.\n\tThe external synchronization timing.\n\n"
			f"\tstart_timestamp_offset_usec: {self._handle.start_timestamp_offset_usec} us. \n\tStart timestamp offset.\n\n"
			)
		return message