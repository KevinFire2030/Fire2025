import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kiwoom Login
        self.kiwoom = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect(int)",0)

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)

        self.setWindowTitle("계좌 정보")
        self.setGeometry(300, 300, 300, 150)

        btn1 = QPushButton("계좌 얻기", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):

        # 모의투자 계좌 1개
        # account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        # self.text_edit.append("계좌번호: " + account_num)


        # 실전투자 계좌 3개
        account_cnt = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")

        self.text_edit.append("계좌갯수: " + account_cnt)

        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO").split(';')

        for i in range(0, int(account_cnt)):
            self.text_edit.append("계좌번호: " + account_num[i])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


