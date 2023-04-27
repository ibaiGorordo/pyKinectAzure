import sys
import numpy as np

rng = np.random.default_rng()

sys.path.insert(1, '../')
import pykinect_azure as pykinect

def rand_int(size):
	return rng.integers(0, 100, size=size)

def check_float2_t(float_val, real_val):
	assert float_val.xy.x == real_val[0]
	assert float_val.xy.y == real_val[1]
	assert float_val.v[0] == real_val[0]
	assert float_val.v[1] == real_val[1]

def check_float3_t(float_val, real_val):
	assert float_val.xyz.x == real_val[0]
	assert float_val.xyz.y == real_val[1]
	assert float_val.xyz.z == real_val[2]
	assert float_val.v[0] == real_val[0]
	assert float_val.v[1] == real_val[1]
	assert float_val.v[2] == real_val[2]

def check_quat_t(quat_val, real_val):
	assert quat_val.wxyz.w == real_val[0]
	assert quat_val.wxyz.x == real_val[1]
	assert quat_val.wxyz.y == real_val[2]
	assert quat_val.wxyz.z == real_val[3]
	assert quat_val.v[0] == real_val[0]
	assert quat_val.v[1] == real_val[1]
	assert quat_val.v[2] == real_val[2]
	assert quat_val.v[3] == real_val[3]

def check_joint_t(joint_val, real_pos, real_quat, real_conf):
	check_float3_t(joint_val.position, real_pos)
	check_quat_t(joint_val.orientation, real_quat)
	assert joint_val.confidence_level == real_conf

def check_joint2d_t(joint_val, real_pos, real_conf):
	check_float2_t(joint_val.position, real_pos)
	assert joint_val.confidence_level == real_conf

def check_skeleton_t(skeleton_val, real_pos_array, real_quat_array, real_conf_array):
	for i in range(pykinect.K4ABT_JOINT_COUNT):
		check_joint_t(skeleton_val.joints[i], real_pos_array[i], real_quat_array[i], real_conf_array[i])

def check_skeleton2d_t(skeleton_val, real_pos_array, real_conf_array):
	for i in range(pykinect.K4ABT_JOINT_COUNT):
		check_joint2d_t(skeleton_val.joints2D[i], real_pos_array[i], real_conf_array[i])

def test_float2_t():
	pos_xy = rand_int(2)
	float2_val = pykinect.k4a_float2_t(pos_xy)
	check_float2_t(float2_val, pos_xy)

def test_float3_t():
	pos_xyz = rand_int(3)
	float3_val = pykinect.k4a_float3_t(pos_xyz)
	check_float3_t(float3_val, pos_xyz)

def test_quaternion_t():
	quat = rand_int(4)
	quat_val = pykinect.k4a_quaternion_t(quat)
	check_quat_t(quat_val, quat)

def test_joint_t():
	joint_pos = rand_int(3)
	joint_quat = rand_int(4)
	joint_conf = rand_int(1)[0]
	joint_val = pykinect.k4abt_joint_t(joint_pos,joint_quat, joint_conf)
	check_joint_t(joint_val, joint_pos, joint_quat, joint_conf)

def test_joint2d_t():
	joint2d_pos = rand_int(2)
	joint2d_conf = rand_int(1)[0]
	joint2d_val = pykinect.k4abt_joint2D_t(joint2d_pos, joint2d_conf)
	check_joint2d_t(joint2d_val, joint2d_pos, joint2d_conf)

def test_skeleton_t():
	skeleton_pos_array = [rand_int(3) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_quat_array = [rand_int(4) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_conf_array = rand_int(pykinect.K4ABT_JOINT_COUNT)
	joints = [pykinect.k4abt_joint_t(skeleton_pos_array[i], skeleton_quat_array[i], skeleton_conf_array[i]) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_val = pykinect.k4abt_skeleton_t(joints)
	check_skeleton_t(skeleton_val, skeleton_pos_array, skeleton_quat_array, skeleton_conf_array)

def test_skeleton2d_t():
	skeleton2d_pos_array = [rand_int(2) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton2d_conf_array = rand_int(pykinect.K4ABT_JOINT_COUNT)
	joints = [pykinect.k4abt_joint2D_t(skeleton2d_pos_array[i], skeleton2d_conf_array[i]) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton2d_val = pykinect.k4abt_skeleton2D_t(joints)
	check_skeleton2d_t(skeleton2d_val, skeleton2d_pos_array, skeleton2d_conf_array)

def test_body_t():
	body_id = rand_int(1)[0]
	skeleton_pos_array = [rand_int(3) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_quat_array = [rand_int(4) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_conf_array = rand_int(pykinect.K4ABT_JOINT_COUNT)
	joints = [pykinect.k4abt_joint_t(skeleton_pos_array[i], skeleton_quat_array[i], skeleton_conf_array[i]) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton_val = pykinect.k4abt_skeleton_t(joints)
	body_val = pykinect.k4abt_body_t(body_id, skeleton_val)
	assert body_val.id == body_id
	check_skeleton_t(body_val.skeleton, skeleton_pos_array, skeleton_quat_array, skeleton_conf_array)

def test_body2d_t():
	body_id = rand_int(1)[0]
	skeleton2d_pos_array = [rand_int(2) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton2d_conf_array = rand_int(pykinect.K4ABT_JOINT_COUNT)
	joints = [pykinect.k4abt_joint2D_t(skeleton2d_pos_array[i], skeleton2d_conf_array[i]) for i in range(pykinect.K4ABT_JOINT_COUNT)]
	skeleton2d_val = pykinect.k4abt_skeleton2D_t(joints)
	body2d_val = pykinect.k4abt_body2D_t(body_id, skeleton2d_val)
	assert body2d_val.id == body_id
	check_skeleton2d_t(body2d_val.skeleton, skeleton2d_pos_array, skeleton2d_conf_array)

def test_empty_values():
	float2_val = pykinect.k4a_float2_t()
	check_float2_t(float2_val, [0,0])

	float3_val = pykinect.k4a_float3_t()
	check_float3_t(float3_val, [0,0,0])

	quat_val = pykinect.k4a_quaternion_t()
	check_quat_t(quat_val, [0,0,0,0])

	joint_val = pykinect.k4abt_joint_t()
	check_joint_t(joint_val, [0,0,0], [0,0,0,0], 0)

	joint2d_val = pykinect.k4abt_joint2D_t()
	check_joint2d_t(joint2d_val, [0,0], 0)

	skeleton_val = pykinect.k4abt_skeleton_t()
	check_skeleton_t(skeleton_val, [[0,0,0] for i in range(pykinect.K4ABT_JOINT_COUNT)], [[0,0,0,0] for i in range(pykinect.K4ABT_JOINT_COUNT)], [0 for i in range(pykinect.K4ABT_JOINT_COUNT)])

	skeleton2d_val = pykinect.k4abt_skeleton2D_t()
	check_skeleton2d_t(skeleton2d_val, [[0,0] for i in range(pykinect.K4ABT_JOINT_COUNT)], [0 for i in range(pykinect.K4ABT_JOINT_COUNT)])

if __name__ == "__main__":

	test_float2_t()
	test_float3_t()
	test_quaternion_t()
	test_joint_t()
	test_joint2d_t()
	test_skeleton_t()
	test_skeleton2d_t()
	test_body_t()
	test_body2d_t()

	test_empty_values()


