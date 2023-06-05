import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

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



        """
        
          [LONG GetLoginInfo()]
          
          로그인 후 사용할 수 있으며 인자값에 대응하는 정보를 얻을 수 있습니다.
          
          인자는 다음값을 사용할 수 있습니다.
          
          "ACCOUNT_CNT" : 보유계좌 갯수를 반환합니다.
          "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
          "USER_ID" : 사용자 ID를 반환합니다.
          "USER_NAME" : 사용자 이름을 반환합니다.
          "GetServerGubun" : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실거래서버)
          "KEY_BSECGB" : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
          "FIREW_SECGB" : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
          
          리턴값
          인자값에 대응하는 정보를 얻을 수 있습니다.
          ------------------------------------------------------------------------------------------------------------------------------------
          
          [보유계좌 목록 예시]
          
          CString   strAcctList = GetLoginInfo("ACCLIST");
          여기서 strAcctList는 ';'로 분리한 보유계좌 목록임
          예) "3040525910;5678905510;3040526010"
          
          -------------------------------------------------------------------------------------------------------
        
        
        """

        # rstrip
        # split
        """
        https://dodomp0114.tistory.com/25?category=978327
        
        strip 함수
        - 문자열의 왼쪽, 오른쪽에 있는 공백을 지워주는 함수.        
          syntax : method.strip()
        
        rstrip() : 문자열 왼쪽에 해당하는 공백만 삭제.
        lstrip() : 문자열 오른쪽에 해당하는 공백만 삭제. 
        strip(""), strip('') 처럼 따옴표 안에 제거 하고 싶은 문자 입력시, 해당 문자가 제거됨.
        
        ex)
        >>> A = "   Hello   "
        >>> B = A.strip()
        >>> print (B)
        Hello
        
        # strip 함수에 좌우로 삭제하고 싶은 파라미터 입력.
        >>> A = "@@@HAPPY@@@"
        >>> B = A.strip("@")
        >>> print (B)
        HAPPY
        
        # lstrip 함수 사용, strip("") 활용. ( 문자열 왼쪽에 해당하는 공백/문자 삭제. )
        >>> A = "@@@HAPPY@@@"
        >>> B = A.lstrip("@")
        >>> print (B)
        HAPPY@@@
        
        # rstrip 함수 사용, strip("") 활용. ( 문자열 오른쪽에 해당하는 공백/문자 삭제. )
        >>> A = "@@@HAPPY@@@"
        >>> B = A.rstrip("@")
        >>> print (B)
        @@@HAPPY
        
        
        split 함수
 

        - 문자열 안에 있는 내용을 일정한 규칙으로 구분하여 리스트로 제작해주는 함수.
        
         
        
        syntax : method.split("sep","maxsplit")
        
         
        
        ● sep : 문자열 안의 문자와 문자사이를 어떤 기준으로 나눌지 정해주는 파라미터.
        
                   기본값은 공백을 기준으로 나누어 줌.
        
                    
        
        ● maxsplit : sep 기호를 바탕으로 왼쪽부터 몇번 나눌 것인지 정해주는 파라미터,
        
                         파라미터로는 숫자가 들어가며, 기본값은 -1.
        
         
        
        ex)
        
        >>> A = "Hello,welcome,to,my,blog"
        >>> A.split()
        >>> A.split(',')
        >>> A.split(',',3)
        
        'Hello,welcome,to,my,blog'
        ['Hello', 'welcome', 'to', 'my', 'world']
        ['Hello', 'welcome', 'to', 'my,world']
        
        """
        #self.text_edit.append("계좌번호: " + account_num.rstrip(';'))

        #
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO").split(';')

        self.text_edit.append("계좌번호: " + account_num[1])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()