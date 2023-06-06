import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *


import win32gui
import win32con
import win32api
import time


#--------------------------------------------------------------------
# 수동 로그인 관련 변수와 함수
#--------------------------------------------------------------------

user_id = "iami15"
user_pass = "hoya1515!!"
user_cert = "hoya1515!!"
#user_cert = None
account_pass = "0000"
def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def enum_windows():
    windows = []
    win32gui.EnumWindows(window_enumeration_handler, windows)
    return windows


def find_window(caption):
    hwnd = win32gui.FindWindow(None, caption)
    if hwnd == 0:
        windows = enum_windows()
        for handle, title in windows:
            if caption in title:
                hwnd = handle
                break
    return hwnd


def enter_keys(hwnd, data, interval=500):
    win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
    win32api.SendMessage(hwnd, win32con.EM_REPLACESEL, 0, data)
    win32api.Sleep(interval)


def click_button(btn_hwnd):
    win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    win32api.Sleep(100)
    win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONUP, 0, 0)
    win32api.Sleep(300)


def left_click(x, y, hwnd):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)


def double_click(x, y, hwnd):
    left_click(x, y, hwnd)
    left_click(x, y, hwnd)
    win32api.Sleep(300)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.login_status = False

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect(int)", 0)  # 로그인창 실행
        self.ocx.OnEventConnect.connect(self.event_connect)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        self.auto_login(user_id, user_pass, user_cert)

    def event_connect(self, err_code):
        if err_code == 0:
            self.login_status = True
            self.text_edit.append("로그인 성공")
            self.save_account_pw(account_pass)

    def slot_login(self, err_code):
        print(err_code)

    def auto_login(self, user_id, user_pass, user_cert=None):

        print('auto_login')

        while not self.login_status:

            caption = "영웅문W Login"
            hwnd = find_window(caption)

            if hwnd == 0:
                print("로그인 창 대기 ...")
                time.sleep(1)
                continue
            else:
                break

        time.sleep(2)
        edit_id = win32gui.GetDlgItem(hwnd, 0x3E8)
        edit_pass = win32gui.GetDlgItem(hwnd, 0x3E9)
        edit_cert = win32gui.GetDlgItem(hwnd, 0x3EA)
        btn_login = win32gui.GetDlgItem(hwnd, 0x1)

        if user_cert is None:
            if win32gui.IsWindowEnabled(win32gui.GetDlgItem(hwnd, 0x3EA)):
                click_button(win32gui.GetDlgItem(hwnd, 0x3ED))
        else:
            if not win32gui.IsWindowEnabled(win32gui.GetDlgItem(hwnd, 0x3EA)):
                click_button(win32gui.GetDlgItem(hwnd, 0x3ED))



        double_click(15, 15, edit_pass)
        enter_keys(edit_pass, user_pass)
        time.sleep(0.5)

        if user_cert is not None:
            double_click(15, 15, edit_cert)
            enter_keys(edit_cert, user_cert)
            time.sleep(0.5)

        click_button(btn_login)

    def save_account_pw(self, user_pw):


        self.ocx.dynamicCall("GetCommonFunc(QString, QString)", "ShowAccountWindow", "")



        while True:

            print(user_pw)

            caption = "계좌번호관리"
            hwnd = find_window(caption)

            if hwnd == 0:
                print("계좌번호관리 창 대기 ...")
                time.sleep(1)
                continue
            else:
                break

        time.sleep(2)

        #caption = "계좌번호관리"
        #hwnd = find_window(caption)

        """
        rect = win32gui.GetWindowRect(hwnd)  # 계좌번호관리 창의 좌상단 좌표 찾기
        #pyautogui.click(rect[0] + 104, rect[1] + 72)  # 나열된 계좌번호 중 처번째 클릭
        edit_account = win32gui.GetDlgItem(hwnd, 0x3EA)  # 계좌번호 클릭시 나타나는 좌하단 계좌번호 표시 edit의 핸들 얻기
        edit_pw2 = win32gui.GetDlgItem(hwnd, 0x3E9)  # 계좌암호 edit의 핸들 얻기
        user_account = win32gui.GetWindowText(edit_account)  # 계좌번호 읽어들이기
        win32gui.SendMessage(edit_pw2, win32con.WM_SETTEXT, 0, user_pw)  # 계좌암호 user_pw2 입력
        """

        edit_pass = win32gui.GetDlgItem(hwnd, 0x3E9)
        btn_save_all = win32gui.GetDlgItem(hwnd, 0x3EC)
        btn_close = win32gui.GetDlgItem(hwnd, 0x2)

        double_click(15, 15, edit_pass)
        enter_keys(edit_pass, user_pw)
        time.sleep(0.5)

        click_button(btn_save_all)
        time.sleep(0.5)

        click_button(btn_close)
        time.sleep(0.5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()



