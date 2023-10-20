import base64
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import datetime
import replicate
import os 
from dotenv import load_dotenv
import urllib.request


load_dotenv()
# 현재 날짜와 시간을 포맷팅하여 파일명 생성
current_datetime = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')


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


def caricature(style, my_img):

    output = replicate.run(
        "412392713/vtoonify:54daf6387dc7c4d41ed5238e28e06277a6ee9027af5cd16486b7e0c261ba2522",
        input={"image": open(my_img, "rb"),
               "style_degree": float(style)}
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