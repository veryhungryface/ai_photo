import gradio as gr
from PIL import Image
import os
from dotenv import load_dotenv
import base64
import requests
from io import BytesIO
import numpy as np
import datetime
import replicate
import urllib.request
import smtplib  # SMTP 사용을 위한 모듈
import re  # Regular Expression을 활용하기 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage  # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈

load_dotenv()


pw = os.getenv('BTY_PASS')


method1 = "webcam"
method2 = "upload"

# 현재 날짜와 시간을 포맷팅하여 파일명 생성
current_datetime = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')




# 메일보내기 세팅

# 메일보낼 파일 경로
file_path = './result/temp.png'

# 파일이 존재하는 경우에만 삭제
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File {file_path} has been deleted.")
else:
    print(f"File {file_path} does not exist, so it wasn't deleted.")


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
    msg["Subject"] = "PHOTO BY 2023 인천수학축전-인공지능수학"  # 메일 제목
    msg["From"] = my_account
    msg["To"] = to_mail
    
    # 메일 본문 내용
    content = "안녕하세요. 오늘 즐거우셨나요? 오늘 생성한 사진을 보내드립니다^^ \n\n 언제나 행복하세요^^ \n\n\n -- 2023 인천수학축전-인공지능수학 드림"
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



# 이미지모델 함수
def animegan_file(my_image):
    with open(my_image, 'rb') as image_file:
        # 픽셀데이터 -> base64
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        response = requests.post("https://akhaliq-animeganv1.hf.space/run/predict", json={
            "data": [
                f"data:image/png;base64,{image_base64}",
            ]
        }).json()

        # 응답에서 base64인코딩 파트 추출
        response = response["data"][0].split(",")[1]
        
        # base64 -> 이미지 데이터로 디코딩
        image_data = base64.b64decode(response) #bytes type
        dataBytesIO = BytesIO(image_data) #IObytes type
        image = Image.open(dataBytesIO) 
        image.save('./result/temp.png', 'PNG')
        result = np.array(image) #array type

        return result


def swap(target_img, my_img):

    output = replicate.run(
        "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d",
        input={"target_image": open(target_img, "rb"),
            "swap_image": open(my_img, "rb")}
    )

    # 결과이미지를 다운로드
    file_name = f"photo_{current_datetime}.png"
    urllib.request.urlretrieve(output, f'./result/{file_name}')
    image = Image.open(f'./result/{file_name}')
    image.save('./result/temp.png', 'PNG')
    # 이미지를 NumPy 배열로 변환
    image_array = np.array(image)

    return image_array        


def caricature(style_type, style_degree, my_img):

    output = replicate.run(
        "412392713/vtoonify:54daf6387dc7c4d41ed5238e28e06277a6ee9027af5cd16486b7e0c261ba2522",
        input={"image": open(my_img, "rb"),
               "style_type": style_type,
               "style_degree": float(style_degree)}
    )

    # 결과이미지를 다운로드
    file_name = f"photo_{current_datetime}.png"
    urllib.request.urlretrieve(output, f'./result/{file_name}')
    image = Image.open(f'./result/{file_name}')
    image.save('./result/temp.png', 'PNG')
    # 이미지를 NumPy 배열로 변환
    image_array = np.array(image)

    return image_array

def cartoon(my_img):

    output = replicate.run(
        "catacolabs/cartoonify:f109015d60170dfb20460f17da8cb863155823c85ece1115e1e9e4ec7ef51d3b",
        input={"image": open(my_img, "rb")}
    )

    # 결과이미지를 다운로드
    file_name = f"photo_{current_datetime}.png"
    urllib.request.urlretrieve(output, f'./result/{file_name}')
  
    image = Image.open(f'./result/{file_name}')
    image.save('./result/temp.png', 'PNG')
    # 이미지를 NumPy 배열로 변환
    image_array = np.array(image)

    return image_array


def img2sketch_file(my_image):
    with open(my_image, 'rb') as image_file:
        # 이미지데이터 -> base64 인코딩
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # API요청 보내기
        response = requests.post("https://hossay-image-to-sketch.hf.space/run/predict", json={
            "data": [
                f"data:image/png;base64,{image_base64}"
            ]
        }).json()

        # 응답에서 base64인코딩 파트 추출
        response = response["data"][0].split(",")[1]
        
        # base64 -> 이미지 데이터로 디코딩
        image_data = base64.b64decode(response) #bytes type
        dataBytesIO = BytesIO(image_data) #IObytes type
        image = Image.open(dataBytesIO) 
        image.save('./result/temp.png', 'PNG')
        result = np.array(image) #array type

        return result


#gradio에서 사용할 함수

def sendmail_(receiver):
    message = sendmail(receiver, './result/temp.png')
    print(message)
    return message 

def count_files(name):
    if not os.path.exists('./example') or not os.path.isdir('./example'):
        print(f"The folder '{name}' does not exist or is not a directory.")
        return

    file_count = 0
    for filename in os.listdir('./example'):
        if filename.startswith(name) and filename.endswith(".png"):
            file_count += 1
    return file_count

def poster_gen(face, poster_num):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = swap(f'./example/poster{int(poster_num)}.png', f'./image/temp.png')
    
    return result

def hero_gen(face, hero_num):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = swap(f'./example/hero{hero_num}.png', f'./image/temp.png')
    
    return result

def album_gen(face, poster_num):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = swap(f'./example/album_{int(poster_num)}.png', f'./image/temp.png')
    
    return result

def cari_gen(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = animegan_file('./image/temp.png')
    
    return result

def cari_gen2(face, style_type, style_degree):
    im = Image.fromarray(face)
    im.save('./image/temp.png')

    if style_type == "3d만화":
        style_type="cartoon1"
    elif style_type == "픽사에니메이션":
        style_type="pixar"       
    elif style_type == "눈코입강렬":
        style_type="comic1-d"        
    elif style_type == "캐리_입강조":
        style_type="caricature1"
    elif style_type == "캐리_상남자":
        style_type="arcane2"

    result = caricature(style_type ,style_degree, f'./image/temp.png')
    
    return result

def cari_gen3(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = cartoon(f'./image/temp.png')
    
    return result

def sketch_gen(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = img2sketch_file('./image/temp.png')
    
    return result



poster_files = count_files('poster')
hero_files = count_files('hero')
cari1_files = count_files('cari1')
cari2_files = count_files('cari2')
cari3_files = count_files('cari3')
sketch_files = count_files('sketch')
album_files = count_files('album')

# # load images in 'example' folder as examples
# example_folder = os.path.join(os.path.dirname(__file__), 'example')
# example_fns = os.listdir(example_folder)
# example_fns.sort()
# examples_full = [os.path.join(example_folder, x) for x in example_fns if x.endswith('.png')]

EXAMPLES_poster = [f"example/poster{i+1}.png" for i in range(poster_files)]
EXAMPLES_hero = [f"example/hero{i+1}.png" for i in range(hero_files)]
EXAMPLES_cari1 = [f"example/cari1_{i+1}.png" for i in range(cari1_files)]
EXAMPLES_cari2 = [f"example/cari2_{i+1}.png" for i in range(cari2_files)]
EXAMPLES_cari3 = [f"example/cari3_{i+1}.png" for i in range(cari3_files)]
EXAMPLES_sketch = [f"example/sketch{i+1}.png" for i in range(sketch_files)]
EXAMPLES_album = [f"example/album_{i+1}.png" for i in range(album_files)]


# Gradio UI

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Row(variant='panel'):
        with gr.Column(variant='panel'):
            gr.Markdown(
            """
            # 2023 인천수학축전
            # 인공지능 수학 AI PHOTO 
            **상업적이용시 저작권 문제가 발생할 수 있습니다. 재미로 봐주세요^^
            """)
        with gr.Column(variant='panel'):
            with gr.Row():
                with gr.Column():
                    receiver = gr.Text(label="받는 메일주소 **공공기관 메일은 X")
                with gr.Column():
                    btn = gr.Button("방금 생성한 사진 전송")
        with gr.Column(variant='panel'):
                    txt = gr.Text(label='전송결과')
                
                    btn.click(fn=sendmail_,
                        inputs=receiver,
                        outputs=txt)    

    with gr.Tab("웹캠"):    
        with gr.Row(variant='panel'):
            with gr.Tab("영화포스터"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )

                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=poster_gen,
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_poster), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                            
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_poster,
                                inputs=image_upload,
                                
                                label="포스터",
                                
                            )
                    
            with gr.Tab("영웅"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=hero_gen,
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_hero), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                            
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_hero,
                                inputs=image_upload,
                                
                                label="영웅",
                                
                            )
            with gr.Tab("졸업앨범"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=album_gen,
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_album), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_album,
                                inputs=image_upload,
                                
                                label="앨범 쌤플",
                                
                            )   
                            
            with gr.Tab("수채화"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=cari_gen,
                            inputs=gr.Image(source=method1),
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari1,
                                inputs=image_upload,
                                
                                label="수채화 쌤플",
                                
                            )
                    
            with gr.Tab("캐리커쳐"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=cari_gen2,
                            inputs=[gr.Image(source=method1), gr.Radio(["3d만화", "픽사에니메이션", "눈코입강렬" , "캐리_입강조", "캐리_상남자"], label="캐리커처Style", value="3d만화"), gr.Slider(0, 1, step=0.1, value=0.5)],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari2,
                                inputs=image_upload,
                                
                                label="캐리커쳐 쌤플",
                                
                            )
                    
                             
            with gr.Tab("스케치"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=sketch_gen,
                            inputs=gr.Image(source=method1),
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_sketch,
                                inputs=image_upload,
                                
                                label="스케치 쌤플",
                                
                            )
          
            

    with gr.Tab("업로드"):
        with gr.Row(variant='panel'):
            with gr.Tab("영화포스터"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )

                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=poster_gen,
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_poster), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                            
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_poster,
                                inputs=image_upload,
                                
                                label="포스터",
                                
                            )
                    
            with gr.Tab("영웅"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=hero_gen,
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_hero), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                            
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_hero,
                                inputs=image_upload,
                                
                                label="영웅",
                                
                            )
            with gr.Tab("졸업앨범"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=album_gen,
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_album), step=1) ],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_album,
                                inputs=image_upload,
                                
                                label="앨범",
                                
                            )    
                            
            with gr.Tab("수채화"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=cari_gen,
                            inputs=gr.Image(source=method1),
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari1,
                                inputs=image_upload,
                                
                                label="수채화 쌤플",
                                
                            )
                    
            with gr.Tab("캐리커쳐"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=cari_gen2,
                            inputs=[gr.Image(source=method1), gr.Radio(["3d만화", "픽사에니메이션", "눈코입강렬" , "캐리_입강조", "캐리_상남자"], label="캐리커처Style", value="3d만화"), gr.Slider(0, 1, step=0.1, value=0.5)],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari2,
                                inputs=image_upload,
                                
                                label="캐리커쳐 쌤플",
                                
                            )
                                        
            with gr.Tab("스케치"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row()
                        
                        with gr.Row():
                            image_upload = gr.Image(
                                label="image_upload",
                                type="pil",
                                elem_id="image_upload",
                                height=1
                            )


                    with left_column:            
                        with left_first_row:
                            gr.Interface(
                            fn=sketch_gen,
                            inputs=gr.Image(source=method2),
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     
                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_sketch,
                                inputs=image_upload,
                                
                                label="스케치 쌤플",
                                
                            )
              
                    

demo.launch(share=True)