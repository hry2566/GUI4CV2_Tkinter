import os
import subprocess
import time

import cv2


class CameraBase():
    def __init__(self):
        pass

    def __decode_fourcc(self, v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

    def __run_shell(self, cmd_array):
        cmd_str = ''
        for cmd in cmd_array:
            cmd_str += f'{cmd};'
        stream = os.popen(cmd)
        return stream.read().split('\n')

    def set_fps(self, cap, device_name, fps):
        cmd_array = []
        cmd_array.append(f'v4l2-ctl -d {device_name} -p {fps}')
        output = self.__run_shell(cmd_array)
        return output

    def get_current_fps(self, cap, device_name):
        cmd_array = []
        cmd_array.append(f'v4l2-ctl -d {device_name} -P')
        output = self.__run_shell(cmd_array)

        for line in output:
            if 'Frames per second:' in line:
                fps = int(line.strip().split(':')[
                          1].split('(')[0].split('.')[0])
                return fps

    def get_current_size(self, cap):
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def get_current_format(self, cap):
        camera_format = self.__decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
        return camera_format

    def get_devices_list(self):
        cmd_array = []
        cmd_array.append('v4l2-ctl --list-devices')
        output = self.__run_shell(cmd_array)

        devices = []
        for device_name in output:
            if ('/dev/video' in device_name) and not (':' in device_name) and not (device_name.strip() == ''):
                device_num = int(device_name.replace('/dev/video', ''))
                cap = cv2.VideoCapture(device_num)
                if cap.isOpened():
                    devices.append(device_name.strip())
        return devices

    def get_devices_list_windows(self):
        cur_dir = os.getcwd()
        cur_dir = cur_dir.replace('\\', '/')
        cmd = f'{cur_dir}/lib/v4w2-ctl/v4w2-ctl --list-devices'
        resoult = subprocess.run(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = resoult.stdout.split('\n')
        devices = []
        for device_name in output:
            if ('/dev/video' in device_name) and not (':' in device_name) and not (device_name.strip() == ''):
                device_num = int(device_name.replace('/dev/video', ''))
                cap = cv2.VideoCapture(device_num)
                if cap.isOpened():
                    devices.append(device_name.strip())
        return devices

    def get_video_formats_list(self, cap,  device_name):
        video_formats = []
        if cap.isOpened():
            cmd_array = []
            cmd_array.append(f'v4l2-ctl -d {device_name} --list-formats-ext')
            output = self.__run_shell(cmd_array)

            for line in output:
                trim = line.strip()
                if ']:' in trim:
                    video_formats.append(trim.split('(')[0].split('\'')[1])
        return video_formats

    def get_video_formats_list_windows(self, cap,  device_name):
        video_formats = []
        if cap.isOpened():
            cur_dir_old = os.getcwd()
            cur_dir = cur_dir_old.replace('\\', '/')
            cmd = f'{cur_dir}/lib/v4w2-ctl/v4w2-ctl -d {device_name} --list-formats-ext'

        result = subprocess.run(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = result.stdout.split('\n')
        for line in output:
            trim = line.strip()
            if ']:' in trim:
                video_formats.append(trim.split('(')[0].split('\'')[1])
        return video_formats

    def get_video_size_list(self, cap,  device_name, video_format):
        video_formats = []
        video_format_get = ''
        if cap.isOpened():
            cmd_array = []
            cmd_array.append(f'v4l2-ctl -d {device_name} --list-formats-ext')
            output = self.__run_shell(cmd_array)

            for index, line in enumerate(output):
                trim = line.strip()
                if ']: ' in trim:
                    video_format_get = trim.split('\'')[1]
                if video_format_get == video_format:
                    if 'Size: Discrete' in trim:
                        height = trim.split('x')[-1]
                        width = trim.split('x')[0].split(' ')[-1]
                        for i in range(index+1, len(output)-1):
                            if 'Interval: Discrete' in output[i]:
                                spl = output[i].split(' ')
                                fps = int(
                                    spl[len(spl)-2].replace('(', '').replace('.000', ''))
                                video_formats.append(
                                    [video_format, width, height, fps])
                                pass
                            else:
                                break
        return video_formats

    def get_video_size_list_windows(self, cap,  device_name, video_format):
        video_formats = []
        video_format_get = ''
        if cap.isOpened():
            cur_dir_old = os.getcwd()
            cur_dir = cur_dir_old.replace('\\', '/')
            cmd = f'{cur_dir}/lib/v4w2-ctl/v4w2-ctl -d {device_name} --list-formats-ext'

            result = subprocess.run(
                cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.split('\n')

            for index, line in enumerate(output):
                trim = line.strip()
                if ']: ' in trim:
                    video_format_get = trim.split('\'')[1]
                if video_format_get == video_format:
                    if 'Size: Discrete' in trim:
                        height = trim.split('x')[-1]
                        width = trim.split('x')[0].split(' ')[-1]
                        for i in range(index+1, len(output)-1):
                            if 'Interval: Discrete' in output[i]:
                                spl = output[i].split(' ')
                                fps = int(
                                    spl[len(spl)-2].replace('(', '').replace('.000', ''))
                                video_formats.append(
                                    [video_format, width, height, fps])
                                pass
                            else:
                                break
        return video_formats

    def get_fps(self, cap):
        time_ms = 5000
        img_array = []
        start = time.time()
        finish = start
        while ((finish-start)*1000 < time_ms):
            _, img = cap.read()
            img_array.append(img)
            finish = time.time()
        return len(img_array)/(time_ms/1000)


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    camera = CameraBase()
    # print(camera.get_devices_list_windows())
    # print(camera.get_devices_list())
    # print(camera.get_video_formats_list(cap, '/dev/video0'))
    # print(camera.get_video_formats_list_windows(cap, '/dev/video0'))
    # print(camera.get_video_size_list(cap, '/dev/video0', 'MJPG'))
    print(camera.get_video_size_list_windows(cap, '/dev/video0', 'MJPG'))
    # print(camera.get_current_format(cap))
    # print(camera.get_current_size(cap))
    # camera.get_current_fps(cap, '/dev/video4')
    # print(camera.set_fps(cap, '/dev/video4', 118))
