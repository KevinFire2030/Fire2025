import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # 윈도우 생성과 동시에 로그인 창도 함께 화면에 표시
        self.kiwoom.dynamicCall("CommConnect()")

        # QTextEdit 객체는 최상위 운도우 안으로 생성돼야 하므로 QTextEdit 객체를 생성할 때 인자로 self 매개변수를 전달
        # 생성된 QTextEdit 객체를 self.text_edit라는 변수가 바인딩
        # self를 사용하는 이유는 클래스의 다른 메서드에서도 해당 변수를 사용해 객체에 접근하기 위함
        self.text_edit = QTextEdit(self)

        # 출력 위치 (10, 60), 크기 조정 (280, 80)
        self.text_edit.setGeometry(10, 60, 280, 80)

        # 읽기/쓰기 모드 변경
        # QTextEdit 위젯은 보통 사용자로부터 어떤 입력을 받는데 사용합니다.
        # 그런데 단순히 정보를 출력하는 용도로 사용하고자 할 때는 setEnabled 메소드를 사용해서 사용자가 입력할 수 없도록 속성을 설정할 수 있습니다.
        self.text_edit.setEnabled(False)

        # 이벤트와 이벤트 처리 메서드 연결
        self.kiwoom.OnEventConnect.connect(self.event_connect)

    def event_connect(self, err_code):
        """
        로그인 처리 이벤트입니다.성공이면 인자값 nErrCode가 0이며 에러는 다음과 같은 값이 전달됩니다.
         nErrCode별 상세내용
          -100 사용자 정보교환 실패
          -101 서버접속 실패
          -102 버전처리 실패
        """

        if err_code == 0:
            self.text_edit.append("로그인 성공")
        elif err_code == 100:
            self.text_edit.append("사용자 정보교환 실패")
        elif err_code == 101:
            self.text_edit.append("서버접속 실패")
        elif err_code == 102:
            self.text_edit.append("버전처리 실패")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()