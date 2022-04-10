import numpy as np
import open3d as o3d

class Open3dVisualizer():

	def __init__(self):

		self.point_cloud = o3d.geometry.PointCloud()
		self.o3d_started = False

		self.vis = o3d.visualization.Visualizer()
		self.vis.create_window()

	def __call__(self, points_3d):

		self.update(points_3d)

	def update(self, points_3d):

		# Process points
		all_points = Open3dVisualizer.process_data(points_3d)

		# Add values to vectors
		self.point_cloud.points = o3d.utility.Vector3dVector(all_points)

		# Add geometries if it is the first time
		if not self.o3d_started:
			self.vis.add_geometry(self.point_cloud)
			self.o3d_started = True

		else:
			self.vis.update_geometry(self.point_cloud)

		self.vis.poll_events()
		self.vis.update_renderer()

	@staticmethod
	def process_data(points_3d_list):

		all_points = points_3d_list
		
		# Fix axis to match open3d
		all_points = -all_points[:,[0,1,2]]
		all_points[:,0] = -all_points[:,0]
		
		return all_points
			