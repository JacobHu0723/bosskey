#include<windows.h>

#pragma comment( linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" ) 

#define KEY_DOWN(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

int main() {
	bool f = false;
	HWND hwnd = ::FindWindow("Chrome_WidgetWin_1"
		,NULL);//获取窗口的句柄 
	HWND hwnd2 = ::GetParent(hwnd);
	while (1) {
		if (KEY_DOWN(VK_MBUTTON)) { //按下鼠标中键
			ShowWindow(hwnd2, f);
			f = 1 - f;
			Sleep(100);
		}
		Sleep(50);
	}
}
