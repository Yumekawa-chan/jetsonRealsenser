import pyrealsense2 as rs

ctx = rs.context()

devices = ctx.query_devices()

for device in devices:
    print("serial_number:", device.get_info(rs.camera_info.serial_number))
    print("asic_serial_number:", device.get_info(
        rs.camera_info.asic_serial_number))
    print("Realsense is correctly connected!")
