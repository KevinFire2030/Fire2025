import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        # 출력 위치 (300, 300), 크기 (300, 150)
        self.setGeometry(300, 300, 300, 150)

        # QLable은 텍스트나 이미지를 출력
        # 텍스트를 출력한다면 생성자의 첫 번째 인자로 출력될 문자열을 전달, 두번째 인자는 부모 위젯을 지정
        # QLable은 QMainWindow 안에 위치하므로 부모 위젯으로 self를 지정
        # QLabel은 텍스트를 출력하는 용도로만 사용되며 다른 메서드에서는 사용되지 않기 때문에
        # self.label이라는 변수로 바인딩하지 않고 label이라는 이름으로 바인딩
        label = QLabel('종목코드: ', self)

        # 출력 위치, 만약 출력 위치와 크기를 동시에 조절하려면 setGeometry 메서드 사용
        label.move(20, 20)

        # QLineEdit 위젯은 생성자뿐만 아니라 다른 메서드에서도 사용될 예정이므로
        # self.code_edit와 같이 self라는 키워드를 붙여서 객체를 바인딩
        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)
        self.code_edit.setText("039490")

        # 출력될 텍스트를 첫 번째 인자로 전달하고, 버튼의 부모 위젯을 두 번째 인자로 전달
        btn1 = QPushButton("조회", self)
        btn1.move(190, 20)


        self.text_edit = QTextEdit(self)
        # 위치 (10, 60), 크기 (280, 80)
        self.text_edit.setGeometry(10, 60, 280, 80)
        # Read Only
        self.text_edit.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()