import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.setWindowTitle("종목 코드")
        self.setGeometry(500, 500, 500, 300)

        btn1 = QPushButton("종목코드 얻기", self)
        btn1.move(350, 10)
        btn1.clicked.connect(self.btn1_clicked)


        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 300, 200)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("GetFutureList()")

        # 리턴 값은 문자열이고 해당 문자열 내에서 각 종목은 세미콜론(;)으로 구분해서 파이썬 리스트 생성
        future_code_list = ret.split(';')
        future_code_name_list = []

        for x in future_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
            future_code_name_list.append(x + " : " + name)

        self.listWidget.addItems(future_code_name_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())