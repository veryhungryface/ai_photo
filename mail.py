import smtplib  # SMTP 사용을 위한 모듈
import re  # Regular Expression을 활용하기 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage  # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈
import os
from dotenv import load_dotenv

load_dotenv()
pw = os.getenv('BTY_PASS')

def sendmail(receiver, my_image):

    def sendEmail(addr):
        reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"  # 유효성 검사를 위한 정규표현식
        if re.match(reg, addr):
            smtp.sendmail(my_account, to_mail, msg.as_string())
            result_msg = f"{to_mail}으로 정상적으로 메일이 발송되었습니다."
        else:
            result_msg = "받으실 메일 주소를 정확히 입력하십시오."
        return result_msg

    # smpt 서버와 연결
    gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    
    # 로그인
    my_account = "sk8erbty@gmail.com"
    my_password = pw
    smtp.login(my_account, my_password)
    
    # 메일을 받을 계정
    to_mail = receiver
    
    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = "PHOTO BY 인천과학예술영재학교 SW.AI 페스티벌"  # 메일 제목
    msg["From"] = my_account
    msg["To"] = to_mail
    
    # 메일 본문 내용
    content = "안녕하세요. 오늘 즐거우셨나요? 오늘 생성한 사진을 보내드립니다^^ \n\n 언제나 행복하세요^^ \n\n\n --인천과학예술영재학교 AI교사연구회 드림"
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)
    
    # 이미지 파일 추가
    image_name = my_image
    with open(image_name, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename=image_name)
        msg.attach(img)
    
    # 받는 메일 유효성 검사 거친 후 메일 전송
    result = sendEmail(to_mail)
    
    # smtp 서버 연결 해제
    smtp.quit()

    return result