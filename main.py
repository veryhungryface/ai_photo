import gradio as gr
import gan 
from PIL import Image
import os
from dotenv import load_dotenv
import mail

load_dotenv()

# 파일 경로
file_path = './result/temp.png'

# 파일이 존재하는 경우에만 삭제
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File {file_path} has been deleted.")
else:
    print(f"File {file_path} does not exist, so it wasn't deleted.")


pw = os.getenv('BTY_PASS')


method1 = "webcam"
method2 = "upload"


def sendmail(receiver):
    message = mail.sendmail(receiver, './result/temp.png')
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
    
    result = gan.swap(f'./example/poster{int(poster_num)}.png', f'./image/temp.png')
    
    return result

def hero_gen(face, hero_num):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.swap(f'./example/hero{hero_num}.png', f'./image/temp.png')
    
    return result

def cari_gen(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.animegan_file('./image/temp.png')
    
    return result

def cari_gen2(face, style):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.caricature(style, f'./image/temp.png')
    
    return result

def cari_gen3(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.cartoon(f'./image/temp.png')
    
    return result

def sketch_gen(face):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.img2sketch_file('./image/temp.png')
    
    return result

def album_gen(face, poster_num):
    im = Image.fromarray(face)
    im.save('./image/temp.png')
    
    result = gan.swap(f'./example/album_{int(poster_num)}.png', f'./image/temp.png')
    
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
    with gr.Row(variant='panel', scale=1):
        gr.Markdown(
        """
        # 인공지능 교사연구회 by IASA
         **상업적이용시 저작권 문제가 발생할 수 있습니다. 재미로 봐주세요^^
        """)
    with gr.Tab("웹캠"):    
        with gr.Row(variant='panel', scale=7):
            with gr.Tab("영화포스터"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_poster), step=1, labels="포스터번호") ],
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
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_hero), step=1, labels="포스터번호") ],
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
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method1), gr.Slider(1, len(EXAMPLES_album), step=1, labels="쌤플번호") ],
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
                            
            with gr.Tab("캐리커쳐1"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                                
                                label="캐리커처 쌤플",
                                
                            )
                    
            with gr.Tab("캐리커쳐2"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method1), gr.Slider(0, 1, step=0.1, value=0.5, labels="style")],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari2,
                                inputs=image_upload,
                                
                                label="캐리커쳐2 쌤플",
                                
                            )
                    
                             
            with gr.Tab("스케치"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
        with gr.Row():
            with gr.Column(scale=2):
                receiver = gr.Text(label="받는 메일주소")
            with gr.Column(scale=1):
                btn = gr.Button("메일보내기")
            with gr.Column(scale=2):
                txt = gr.Text(label='전송결과')
            
                btn.click(fn=sendmail,
                    inputs=receiver,
                    outputs=txt)      
            

    with gr.Tab("업로드"):
        with gr.Row(variant='panel', scale=7):
            with gr.Tab("영화포스터"):
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_poster), step=1, labels="포스터번호") ],
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
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_hero), step=1, labels="포스터번호") ],
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
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method2), gr.Slider(1, len(EXAMPLES_album), step=1, labels="쌤플번호") ],
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
                            
            with gr.Tab("캐리커쳐1"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=gr.Image(source=method2),
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari1,
                                inputs=image_upload,
                                
                                label="캐리커처 쌤플",
                                
                            )
                    
            with gr.Tab("캐리커쳐2"):    
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
                            inputs=[gr.Image(source=method2), gr.Slider(0, 1, step=0.1, value=0.5, labels="style")],
                            outputs="image",    
                            )

                            # webcam_img = gr.Webcam(label="촬영")
                            # num = gr.Slider(1, 8)     

                with gr.Row(variant='panel'):
                    gr.Examples(
                                examples=EXAMPLES_cari2,
                                inputs=image_upload,
                                
                                label="캐리커쳐2 쌤플",
                                
                            )
                                        
            with gr.Tab("스케치"):     
                with gr.Row(variant='panel'):
                    left_column = gr.Column()
                    # right_column = gr.Column()
                    with left_column:
                        left_first_row = gr.Row(scale=3)
                        
                        with gr.Row(scale=1):
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
        with gr.Row():
            with gr.Column(scale=2):
                receiver = gr.Text(label="받는 메일주소")
            with gr.Column(scale=1):
                btn = gr.Button("메일보내기")
            with gr.Column(scale=2):
                txt = gr.Text(label='전송결과')
            
                btn.click(fn=sendmail,
                    inputs=receiver,
                    outputs=txt)    
                
                    

demo.launch()