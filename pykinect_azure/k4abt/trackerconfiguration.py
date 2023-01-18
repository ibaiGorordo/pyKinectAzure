from pykinect_azure.k4abt import _k4abt


class TrackerConfiguration:

    def __init__(self, configuration_handle=None):
        if configuration_handle:
            self._handle = configuration_handle
        else:
            self.create()

    def handle(self):
        return self._handle

    def __setattr__(self, name, value):
        """Run on change function when configuration parameters are changed"""

        if hasattr(self, name):
            if name != "_handle":
                if int(self.__dict__[name]) != value:
                    self.__dict__[name] = value
                    self.on_value_change()
            else:
                self.__dict__[name] = value
        else:
            self.__dict__[name] = value

    def __str__(self):
        """Print the current settings and a short explanation"""
        message = (
            "Device configuration: \n"
            f"\tsensor_orientation: {self.sensor_orientation} \n\t(0: Default, 1: Clockwise90, 2: CounterClockwise90, 3: Flip180)\n\n"
            f"\ttracker_processing_mode: {self.tracker_processing_mode} \n\t(0:Gpu, 1:Cpu, 2:CUDA, 3:TensorRT, 4:DirectML)\n\n"
            f"\tgpu_device_id: {self.gpu_device_id}\n\n"
            f"\tmodel_path: {self.model_path if hasattr(self, 'model_path') else 'Default Model'}"
        )
        return message

    def create(self):
        self.sensor_orientation = _k4abt.K4ABT_SENSOR_ORIENTATION_DEFAULT
        self.tracker_processing_mode = _k4abt.K4ABT_TRACKER_PROCESSING_MODE_GPU
        self.gpu_device_id = 0

        self.on_value_change()

    def create_from_handle(self, tracker_configuration_handle):
        self.sensor_orientation = tracker_configuration_handle.sensor_orientation
        self.tracker_processing_mode = tracker_configuration_handle.tracker_processing_mode
        self.gpu_device_id = tracker_configuration_handle.gpu_device_id
        self.model_path = tracker_configuration_handle.model_path

    def on_value_change(self):
        handle = None
        if hasattr(self, "_model_path"):
            handle = _k4abt.k4abt_tracker_configuration_t(self.sensor_orientation,
                                                                self.tracker_processing_mode,
                                                                self.gpu_device_id,
                                                                self.model_path)
        else:
            handle = _k4abt.k4abt_tracker_configuration_t(self.sensor_orientation,
                                                                self.tracker_processing_mode,
                                                                self.gpu_device_id)
        self._handle = handle


default_tracker_configuration = TrackerConfiguration()
