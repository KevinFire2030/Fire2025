import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)


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

        # btn1 객체에서 'clicked' 이벤트가 발생하면 btn1_clicked 메서드가 호출되도록 설정
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        # 위치 (10, 60), 크기 (280, 80)
        self.text_edit.setGeometry(10, 60, 280, 80)
        # Read Only
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):
        # 입력값 가지오기
        code = self.code_edit.text()
        self.text_edit.append("종목코드: " + code)

        # SetInputValue
        # TR 입력값 설정
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        # CommRqData
        # TR을 서버로 송신
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):

        if rqname == "opt10001_req":

            # 일부 TR에서 사용상 제약이 있음므로 이 함수 대신 GetCommData()함수를 사용하시기 바랍니다.
            # 이   함수는   지원하지   않을   것이므로   용도에   맞는   전용   함수를   사용할   것(비고참고)
            # 조회 정보   요청   - openApi.GetCommData(“OPT00001”, RQName, 0, “현재가”)
            # 실시간정보   요청   - openApi.GetCommRealData(“000660”, 10);
            # 체결정보   요청   - openApi.GetChejanData(9203);

            """
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                             0, "거래량")
            """

            # GetCommData 메서드는 Open API+에서 제공하는 메서드이므로 이를 파이썬 코드에서 사용하려면 dynamicCall 메서드를 사용해야 한다

            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "거래량")

            # strip 메서드를 호출해서 문자열의 공백을 제거
            # '                                          키움증권'
            # '               35121'
            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()