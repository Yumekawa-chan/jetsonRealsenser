import socket
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import json
from datetime import datetime

with open('configs/config.json', 'r') as config_file:
    config_data = json.load(config_file)

jet_id = config_data['jet_id']
host = config_data['host']
port = 65432
resolution_width = config_data['resolution_width']
resolution_height = config_data['resolution_height']


def capture_images():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    config = rs.config()
    pipeline = rs.pipeline()
    config.enable_stream(rs.stream.infrared, 1, resolution_width, resolution_height, rs.format.y8, 30)
    config.enable_stream(rs.stream.infrared, 2, resolution_width, resolution_height, rs.format.y8, 30)
    config.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, 30)

    pipeline.start(config)

    align = rs.align(rs.stream.color)

    try:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()

        spatial = rs.spatial_filter()
        temporal = rs.temporal_filter()
        disparity_filter = rs.disparity_transform()

        depth_frame = spatial.process(depth_frame)
        depth_frame = temporal.process(depth_frame)
        depth_frame = disparity_filter.process(depth_frame)

        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            return

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        np.save(f'./image/depth_{timestamp}_{jet_id}.npy',depth_image)

        cv2.imwrite(f'./image/color_{timestamp}_{jet_id}.png', color_image)
        # cv2.imwrite(f'./image/depth_{timestamp}_{jet_id}.png', depth_image)
        print("Saved!")
    finally:
        pipeline.stop()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print("Connected to server")

    while True:
        data = client_socket.recv(1024).decode()

        if data == 'capture':
            capture_images()
        elif data == 'exit':
            break

finally:
    client_socket.close()
    print("Connection closed")
