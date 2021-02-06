#include<windows.h>

#define KEY_DOWN(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

int main() {
	bool f = false;
	HWND hwnd = ::FindWindow(NULL,"计算器");//获取窗口的句柄 
	while (1) {
		if (KEY_DOWN(VK_MBUTTON)) { //按下鼠标中键
			ShowWindow(hwnd, f);
			f = 1 - f;
			Sleep(100);
		}
		Sleep(20);
	}
}
