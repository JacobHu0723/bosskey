import sys
import json
import subprocess
import keyboard
import win32gui
import win32con
import win32process
import win32api
import psutil
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from PyQt5 import QtWidgets, QtCore


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # 创建全局快捷键
        keyboard.add_hotkey('ctrl+shift+`', self.onKill)
        keyboard.add_hotkey('ctrl+`', self.onHide)

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('BossKey')
        self.resize(400, 250)

        # 设置窗口始终置于顶层
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # 创建两个按钮
        self.killButton = QtWidgets.QPushButton('关闭进程', self)
        self.hideButton = QtWidgets.QPushButton('隐藏/恢复进程', self)

        # 设置按钮的点击事件
        self.killButton.clicked.connect(self.onKill)
        self.hideButton.clicked.connect(self.onHide)

        # 使用垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.killButton)
        vbox.addWidget(self.hideButton)

        self.setLayout(vbox)

    def onKill(self):
        # 读取config.json文件中的进程列表
        with open('config.json', 'r') as f:
            config = json.load(f)
            processes = config['processes']

        # 遍历进程列表，尝试关闭每一个进程
        for process in processes:
            try:
                subprocess.call(['taskkill', '/F', '/IM', process])
            except:
                pass

    def onHide(self):
        # 这里是隐藏和恢复窗口的代码，以及静音和取消静音的代码。
        # 读取配置文件
        with open("config.json", "r") as f:
            config = json.load(f)

        # 获取进程名列表
        process_names = config["processes"]

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

        def mute():
            # 从字典中获取要静音的进程名列表
            mute_list = process_names

            # 获取当前活动的音频会话，也就是正在播放声音的程序
            sessions = AudioUtilities.GetAllSessions()

            # 遍历所有的音频会话
            for session in sessions:
                # 获取音频会话的名称，也就是程序的名称
                name = session.Process and session.Process.name() or "System Sounds"
                # 获取音频会话的音量对象，它实现了ISimpleAudioVolume接口
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                # 获取音频会话的当前音量，它是一个0到1之间的浮点数
                level = volume.GetMasterVolume()
                print(level)
                # 判断音频会话的名称是否在要静音的列表中
                if name in mute_list:
                    # 如果在列表中，判断音量大小
                    # 判断音量是否大于0
                    if level > 0:
                        # 如果大于0，就把音量设置为0，也就是静音
                        volume.SetMasterVolume(0, None)
                        # 打印音频会话的名称和静音状态
                        print(f"{name}: muted")
                    else:
                        # 如果不大于0，就把音量设置为1，也就是最大
                        volume.SetMasterVolume(0.4, None)
                        # 打印音频会话的名称和静音状态
                        print(f"{name}: unmuted")
                else:
                    # 如果不在列表中，就跳过，不做任何操作
                    print(f"{name}: skipped")

        def get_procress_name(hwnd, lParam):
            # 获取窗口进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # 获取进程名
            process_name = get_process_name(pid)
            # print('Get process_name successfully!process_name:', process_name)
            if process_name:
                # print('Get process failed!')
                return process_name
            else:
                return
        aa = name in get_process_name
        print(aa)
        result = aa(hwnd, lParam)
        print(result)
        # 隐藏与取消隐藏回调函数
        def enum_windows_callback(hwnd, lParam):
            process_name = get_procress_name
            # 检查进程名是否在列表中
            if any(name in process_name for name in process_names):
                print(hwnd)
                # 检查窗口是否可见
                if win32gui.IsWindowVisible(hwnd):
                    # 隐藏窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                else:
                    # 显示窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            else:
                print("No one.")
                # pass

        # 枚举所有窗口
        # win32gui.EnumWindows(enum_windows_callback, None)
        # mute()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
