import ctypes

from pykinect_azure.k4a import _k4a


class Calibration:

    def __init__(self, calibration_handle: _k4a.k4a_calibration_t):

        self._handle = calibration_handle
        self.color_params = self._handle.color_camera_calibration.intrinsics.parameters.param
        self.depth_params = self._handle.depth_camera_calibration.intrinsics.parameters.param

    def __del__(self):

        self.reset()

    def __str__(self):

        message = (
            "Rgb Intrinsic parameters: \n"
            f"\tcx: {self.color_params.cx}\n"
            f"\tcy: {self.color_params.cy}\n"
            f"\tfx: {self.color_params.fx}\n"
            f"\tfy: {self.color_params.fy}\n"
            f"\tk1: {self.color_params.k1}\n"
            f"\tk2: {self.color_params.k2}\n"
            f"\tk3: {self.color_params.k3}\n"
            f"\tk4: {self.color_params.k4}\n"
            f"\tk5: {self.color_params.k5}\n"
            f"\tk6: {self.color_params.k6}\n"
            f"\tcodx: {self.color_params.codx}\n"
            f"\tcody: {self.color_params.cody}\n"
            f"\tp2: {self.color_params.p2}\n"
            f"\tp1: {self.color_params.p1}\n"
            f"\tmetric_radius: {self.color_params.metric_radius}\n"
        )
        return message

    def get_matrix(self, camera: _k4a.k4a_calibration_type_t):
        if camera == _k4a.K4A_CALIBRATION_TYPE_COLOR:
            return [[self.color_params.fx, 0, self.color_params.cx],
                    [0, self.color_params.fy, self.color_params.cy],
                    [0, 0, 1]]
        elif camera == _k4a.K4A_CALIBRATION_TYPE_DEPTH:
            return [[self.depth_params.fx, 0, self.depth_params.cx],
                    [0, self.depth_params.fy, self.depth_params.cy],
                    [0, 0, 1]]

    def is_valid(self):
        return self._handle

    def handle(self):
        return self._handle

    def reset(self):
        if self.is_valid():
            self._handle = None

    def convert_3d_to_3d(self, source_point3d: _k4a.k4a_float3_t(),
                         source_camera: _k4a.k4a_calibration_type_t,
                         target_camera: _k4a.k4a_calibration_type_t) -> _k4a.k4a_float3_t():

        target_point3d = _k4a.k4a_float3_t()

        _k4a.VERIFY(
            _k4a.k4a_calibration_3d_to_3d(self._handle, source_point3d, source_camera, target_camera, target_point3d),
            "Failed to convert from 3D to 3D")

        return target_point3d

    def convert_2d_to_3d(self, source_point2d: _k4a.k4a_float2_t,
                         source_depth: float,
                         source_camera: _k4a.k4a_calibration_type_t,
                         target_camera: _k4a.k4a_calibration_type_t) -> _k4a.k4a_float3_t():

        target_point3d = _k4a.k4a_float3_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_2d_to_3d(self._handle, source_point2d, source_depth, source_camera, target_camera,
                                          target_point3d, valid), "Failed to convert from 2D to 3D")

        return target_point3d

    def convert_3d_to_2d(self, source_point3d: _k4a.k4a_float3_t,
                         source_camera: _k4a.k4a_calibration_type_t,
                         target_camera: _k4a.k4a_calibration_type_t) -> _k4a.k4a_float2_t():

        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_3d_to_2d(self._handle, source_point3d, source_camera, target_camera, target_point2d,
                                          valid), "Failed to convert from 3D to 2D")

        return target_point2d

    def convert_2d_to_2d(self, source_point2d: _k4a.k4a_float2_t,
                         source_depth: float,
                         source_camera: _k4a.k4a_calibration_type_t,
                         target_camera: _k4a.k4a_calibration_type_t) -> _k4a.k4a_float2_t():

        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_2d_to_2d(self._handle, source_point2d, source_depth, source_camera, target_camera,
                                          target_point2d, valid), "Failed to convert from 2D to 2D")

        return target_point2d

    def convert_color_2d_to_depth_2d(self, source_point2d: _k4a.k4a_float2_t,
                                     depth_image: _k4a.k4a_image_t) -> _k4a.k4a_float2_t():

        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_color_2d_to_depth_2d(self._handle, source_point2d, depth_image, target_point2d,
                                                           valid), "Failed to convert from Color 2D to Depth 2D")

        return target_point2d
