import pyrealsense2 as rs
import numpy as np
import os
import json

if not os.path.exists("para"):
    os.makedirs("para")

if not os.path.exists("image"):
    os.makedirs("image")

with open('configs/config.json', 'r') as config_file:
    config_data = json.load(config_file)

jet_id = config_data['jet_id']
resolution_width = config_data['resolution_width']
resolution_height = config_data['resolution_height']

config = rs.config()
config.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, 30)
config.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, 30)

pipeline = rs.pipeline()
profile = pipeline.start(config)

frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()
depth_frame = frames.get_depth_frame()

color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
color_camera_matrix = np.array([[color_intrinsics.fx, 0, color_intrinsics.ppx],
                                [0, color_intrinsics.fy, color_intrinsics.ppy],
                                [0, 0, 1]])
color_dist_coeffs = np.array([color_intrinsics.coeffs[i] for i in range(5)])

depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
depth_parameters = np.array([
    depth_intrinsics.fx,  
    depth_intrinsics.fy,  
    depth_intrinsics.ppx, 
    depth_intrinsics.ppy,
    0, 0, 0, 0, 0  
])

np.save(f"para/camera_matrix_{jet_id}.npy", color_camera_matrix)
np.save(f"para/dist_coeff_{jet_id}.npy", color_dist_coeffs)
np.save(f"para/depth_intrinsics_{jet_id}.npy", depth_parameters)

pipeline.stop()

