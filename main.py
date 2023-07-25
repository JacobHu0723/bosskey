import json
import os
import subprocess
import sys
from ctypes import POINTER, cast

import keyboard
# import win32api
import psutil
import win32con
import win32gui
import win32process
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# # 配置日志记录器
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#
# # 记录不同级别的日志信息
# logging.debug('调试信息')
# logging.info('普通信息')
# logging.warning('警告信息')
# logging.error('错误信息')
# logging.critical('严重错误信息')


class MyWindow(QtWidgets.QWidget):
    mute_state = 0
    # print("已重置mute_state为", mute_state)
    # mute_num = 0

    # 检查 config.json 文件是否存在
    if not os.path.exists('config.json'):
        # 如果文件不存在，则创建文件并写入初始信息
        data = {
            "processes": [""]
        }
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)

    def __init__(self):
        super().__init__()
        self.initUI()

        # 创建全局快捷键
        keyboard.add_hotkey('ctrl+shift+`', self.onKill)
        keyboard.add_hotkey('ctrl+`', self.onHide)

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('BossKey')
        self.resize(404, 187)
        # 设置窗口位置
        self.move(2350, 130)

        # 设置窗口始终置于顶层
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # 创建两个按钮
        self.killButton = QtWidgets.QPushButton('关闭进程  (Ctrl+Shift+`)', self)
        self.hideButton = QtWidgets.QPushButton('隐藏/恢复进程  (Ctrl+`)', self)

        # 设置按钮的点击事件
        self.killButton.clicked.connect(self.onKill)
        self.hideButton.clicked.connect(self.onHide)

        # 获取 config.json 文件的绝对路径
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

        # 创建一个 QLabel 控件来显示链接
        self.label = QtWidgets.QLabel(f'<a href="file:///{config_path}">config.json</a>', self)
        self.label.setOpenExternalLinks(True)
        self.label.linkActivated.connect(self.on_link_activated)

        # 使用垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.killButton)
        vbox.addWidget(self.hideButton)
        # vbox.addStretch()
        vbox.addWidget(self.label, alignment=QtCore.Qt.AlignRight)

        self.setLayout(vbox)

    def on_link_activated(self, link):
        # 处理用户点击链接的操作
        file_path = './config.json'
        os.startfile(file_path)

    # 获取指定进程ID的进程名称
    def get_process_name(pid):
        try:
            # print(pid)
            process = psutil.Process(pid)
            # print('Get process successfully!process.name():', process.name())
            return process.name()
        except:
            # print('Get process failed!')
            return None

    def initWindows(hwnd, lParam):
        # 读取配置文件
        with open("config.json", "r") as f:
            config = json.load(f)
        # 获取进程名列表
        process_names = config["processes"]
        # 获取窗口进程ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        # 获取进程名
        process_name = MyWindow.get_process_name(pid)
        if not process_name:
            return
        # 检查进程名是否在列表中
        if any(name in process_name for name in process_names):
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        else:
            pass

    def onKill(self):
        # 读取config.json文件中的进程列表
        with open('config.json', 'r') as f:
            config = json.load(f)
            processes = config['processes']

        # 遍历进程列表，尝试关闭每一个进程
        for process in processes:
            try:
                subprocess.Popen(['taskkill', '/F', '/IM', process], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, shell=True)
            except:
                pass

    def onHide(self):
        # 这里是隐藏和恢复窗口的代码，以及静音和取消静音的代码。
        # 读取配置文件
        with open("config.json", "r") as f:
            config = json.load(f)

        # 获取进程名列表
        process_names = config["processes"]

        # 获取系统音量
        # def get_system_volume() -> float:
        #     """
        #     获取并返回当前系统的音量大小（浮点数）
        #     :return: 当前系统的音量大小（浮点数），范围为0.0到1.0
        #     """
        #     # 获取默认音频设备
        #     devices = AudioUtilities.GetSpeakers()
        #     interface = devices.Activate(
        #         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        #     volume = cast(interface, POINTER(IAudioEndpointVolume))
        #
        #     # 获取当前系统音量
        #     current_volume = volume.GetMasterVolumeLevelScalar()
        #
        #     return current_volume

        # def set_system_volume(volume: float):
        #     """
        #     将系统音量设置为指定的值
        #     :param volume: 要设置的音量值（浮点数），范围为0.0到1.0
        #     """
        #     # 获取默认音频设备
        #     devices = AudioUtilities.GetSpeakers()
        #     interface = devices.Activate(
        #         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        #     volume = cast(interface, POINTER(IAudioEndpointVolume))
        #
        #     # 设置系统音量
        #     volume.SetMasterVolumeLevelScalar(volume, None)

        def mute_system_volume():
            """
            将系统音量设置为静音
            """
            # 获取默认音频设备
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # 设置系统音量为静音
            volume.SetMute(1, None)

        def unmute_system_volume():
            """
            取消系统静音
            """
            # 获取默认音频设备
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # 取消系统静音
            volume.SetMute(0, None)

        def is_system_muted() -> bool:
            """
            返回系统是否处于静音状态
            :return: 系统是否处于静音状态（布尔值）
            """
            # 获取默认音频设备
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            # 获取系统静音状态
            is_muted = volume.GetMute()

            return is_muted

        # 隐藏与取消隐藏回调函数
        def enum_windows_callback(hwnd, lParam):
            # 获取窗口进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # 获取进程名
            process_name = MyWindow.get_process_name(pid)
            # print('Get process_name successfully!process_name:', process_name)
            if not process_name:
                # print('Get process failed!')
                return
            # 检查进程名是否在列表中
            if any(name in process_name for name in process_names):
                # print(hwnd)
                # 检查窗口是否可见
                if win32gui.IsWindowVisible(hwnd):
                    # 隐藏窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                    # MyWindow.mute_num += 1
                    is_muted = is_system_muted()
                    # print(MyWindow.mute_state)
                    if MyWindow.mute_state == 0:
                        if is_muted:
                            # print("系统静音，无操作")
                            MyWindow.mute_state = 1
                        else:
                            # print("系统未静音，操作静音")
                            mute_system_volume()
                            MyWindow.mute_state = 2
                else:
                    # 显示窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    # MyWindow.mute_num += -1
                    # print(MyWindow.mute_state)
                    if MyWindow.mute_state == 1:
                        # print("原先静音，无操作")
                        pass
                    elif MyWindow.mute_state == 2:
                        # print("原先未静音，取消静音")
                        unmute_system_volume()
                    MyWindow.mute_state = 0
            else:
                # print("No one.")
                pass

        # 枚举所有窗口
        win32gui.EnumWindows(enum_windows_callback, None)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('icon.ico'))
    win32gui.EnumWindows(MyWindow.initWindows, None)
    window.show()

    sys.exit(app.exec_())
