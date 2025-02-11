# py01_gpt_clone.py
# GUI를 위한 모듈
from tkinter import * # tkinter 모듈에 있는 모든 클래스, 함수, 변수 등을 다 쓰겠다.
from tkinter.messagebox import * # 모듈 밑에 있는 모듈을 from tkinter import * 로 가져올 수 없음
from tkinter.scrolledtext import *
from tkinter.font import *
# 제미나이를 위한 모듈
import google.generativeai as genai

# 6. 제미나리 API용 구성
genai.configure(api_key='AIzaSyDTRuZSaxtyMK-IxUKB1X2ap5wK8D7663M') # 신청한 API키
model = genai.GenerativeModel('gemini-1.5-flash') # AI 사전훈련된 모델

# 4. 전송버튼 이벤트
def reponseMessage():
    # showinfo('실행','API를 실행합니다!')
    inputText = textMessage.get('1.0', END).replace('\n','').strip()
    print(inputText)
    textMessage.delete('1.0', END)
    # showinfo('결과', inputText) # 다이얼로그, 모달(Modal)창

    if inputText:
        try:
            textResult.insert(END, '유저: ', BOLD)
            textResult.insert(END, f'{inputText}\n\n','user') # 'user' 텍스트 아규먼트

            ai_reponse = model.generate_content(inputText)
            response = ai_reponse.text

            textResult.insert(END, '챗봇: ' , 'bold')
            textResult.insert(END, f'{response}\n\n', 'ai') # 'ai' 텍스트 태그

        except Exception as e:
            textResult.insert(END, f'{str(e)}\n\n','error')
            
        finally:
            textResult.see(END) # 스크롤 텍스트 마지막 위치로 스크롤 다운

# 8. textMessage 위젯에서 엔테를 치면 전송버튼이 클릭
def keypress(event):
    # print(repr(event.char)) # repr을 안쓰면 \r,\x80 표시안됨
    # \r(캐리지 리턴), \n(뉴라인) 혼용해서 사용 \r\n, \n, \r
    if event.char == '\r':
        reponseMessage()

# 11. 종료시 이벤트 처리 함수
def onClosing():
    if askyesno('종료 확인', '정말 종료하시겠습니까?'):
        root.destroy() # 완전 종료

# 1. 메인 윈도우 생성, 초기설정
root = Tk()
root.title('제미나이 챗봇')
root.geometry('730x450')

# 12. 아이콘 변경
# ./image/ 경로는 삭제
root.iconbitmap('./chatbot.ico') # pyinstaller 로 설치할때는 행당 폴더에 복사하고 경로 변경

# 7. 전체에서 사용할 폰트 지정 -> 나눔 고딕
myFont = Font(family='NanumGothic', size=10)
boldFont = Font(family='NanumGothic', size=10, weight=BOLD)

# 2. UI 화면 구성
inputFrame = Frame(root,width=730, height=30, bg='#EFEFEF')
inputFrame.pack(side=BOTTOM, fill=BOTH)

# 3. inputFrame에 들어갈 Entry와 Button 구성
textMessage = Text(inputFrame, width=75, height=1, wrap=WORD, font=myFont)

# 8. 입력창에서 엔터를 치면 keypress 이벤트처리함수 발생
textMessage.bind('<Key>', keypress)
textMessage.pack(side=LEFT, padx=15)

buttonSend = Button(inputFrame, text='전송', bg='green', fg='white',
                    font=myFont, 
                    command=reponseMessage)
buttonSend.pack(side=RIGHT,padx=20, pady=4)

# 5. API호출 결과 메시지 출력될 스크롤기능이 있는 텍스트위젯
textResult = ScrolledText(root, wrap= WORD, bg='#000000', fg='white', font=myFont) # bg='black'
textResult.pack(fill=BOTH, expand=TRUE)

# 10. 스크롤 텍스트에 나올 메세지 디자인
textResult.tag_configure('user', font=boldFont, foreground='yellow')
textResult.tag_configure('ai', font=myFont, foreground='limegreen') # #89F336
textResult.tag_configure('error', font=boldFont, foreground='red')

# 9. 실행 후 바로 입력창에 포커스가 가도록
textMessage.focus_set()

# 11. 종료버튼(X)를 누르면 종료메세지 확인 후 종료
root.protocol("WM_DELETE_WINDOW", onClosing)

# 1. 종료시까지 계속 실행
root.mainloop()