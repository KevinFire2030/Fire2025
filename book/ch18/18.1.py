import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

#from pywinauto import application
from pywinauto.application import Application
from pywinauto import timings
from pywinauto import findwindows
import time
import os

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect(int)",0)        # 로그인창 실행
        self.ocx.OnEventConnect.connect(self.event_connect)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        #self.auto_login()


    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")


    def slot_login(self, err_code):
        print(err_code)

    def auto_login(self):


        time.sleep(3)

        """
        procs = findwindows.find_elements()

        for proc in procs:
            print(f"{proc} / 프로세스 : {proc.process_id}")
        
        """

        app = application.Application().connect(title_re=".*영웅문*.", class_name="#32770")

        dlg = app['영웅문W Login']

        #dlg.print_control_identifiers()

        pass_ctrl = dlg.Edit2
        pass_ctrl.set_focus()
        pass_ctrl.type_keys('hoya1515')

        btn_ctrl = dlg.Button
        btn_ctrl.click()


        #print("ok")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()                         # 이벤트 루프