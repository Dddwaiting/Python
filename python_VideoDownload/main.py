# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15:18:20 2022

@email: iedingyi@163.com
@author: Dddwaiting

@@@ 程序指南：本程序使用open CV2 ,os ,youtube_dl ,PIL等模块,需要自行导入,同时本程序运行的目录中需要有 /tool/ffmpeg.exe ,
            使用视频转字符功能时，需要先删除 /finalVideo ,/imgbear , /imgout3个文件夹，以免发生冲突
@@@ 程序功能：可以通过输入视频真实链接直接下载，已知支持的网站有Bilibili , Youtube等 ,可以自行摸索,须知是真实视频链接,并非直接在浏览器输入栏获取的链接,
@@@         部分网站可以通过网页检查（F12）方式自行获得
@@@ 模块安装命令：pip install os
               pip install pillow
               pip install opencv-python
               pip install youtube_dl
"""
import cv2
import os
import youtube_dl
from PIL import Image, ImageDraw, ImageFont

WIDTH = 80  # 定义输出画面的宽度
HEIGHT = 45  # 定义
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJDYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")  # 所用字符列表


# 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):  # alpha透明度
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 计算灰度
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]  # 不同的灰度对应着不同的字符


# 通过灰度来区分色块
# 该部分以下和灰度值字符画区别所在
def PictureToChar(folder_path, ascii_path, c):
    print("开始将图片转为字符型：")
    # 循环读取逐帧图片
    for icount in range(1, c):
        IMG = folder_path + str(icount) + '.jpg'  # 文件路径
        if os.path.exists(IMG):
            im = Image.open(IMG)
            # 视频分割后图片的长与宽，与合成视频时要相统一,保存下来，合成字符视频时用到
            asciiImage = im
            WIDTH = int(im.width / 6)  # 高度比例为原图的1/6较好，由于字体宽度
            HEIGHT = int(im.height / 15)  # 高度比例为原图的1/15较好，由于字体高度
            im_txt = Image.new("RGB", (im.width, im.height), (255, 255, 255))
            im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
            txt = ""
            colors = []
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    pixel = im.getpixel((j, i))
                    colors.append((pixel[0], pixel[1], pixel[2]))  # 记录像素颜色信息
                    if (len(pixel) == 4):
                        txt += get_char(pixel[0], pixel[1], pixel[2], pixel[3])
                    else:
                        txt += get_char(pixel[0], pixel[1], pixel[2])
                txt += '\n'
                colors.append((255, 255, 255))
            dr = ImageDraw.Draw(im_txt)
            font = ImageFont.load_default().font  # 获取字体
            x = y = 0
            # 获取字体的宽高
            font_w, font_h = font.getsize(txt[1])
            font_h *= 1.37  # 调整后更佳
            # ImageDraw为每个ascii码进行上色
            for i in range(len(txt)):
                if (txt[i] == '\n'):
                    x += font_h
                    y = -font_w
                dr.text([y, x], txt[i], colors[i])
                y += font_w
            # 输出
            name = str(icount) + '.jpg'
            print(name)
            im_txt.save(ascii_path + str(icount) + '.jpg')
    return asciiImage


def charToVideo(ascii_path, asciiImage, path, c, finalVideo_path):
    # 设置视频编码器,这里使用使用MJPG编码器
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # 不同视频编码对应不同视频格式
    if path.endswith(".mp4"):
        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 这里是mp4格式,文件名后缀为.mp4
    elif path.endswith(".avi"):
        fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')  # （例：'I','4','2','0' 对应avi格式）
    elif path.endswith(".flv"):
        fourcc = cv2.VideoWriter_fourcc('F', 'L', 'V', '1')  # 该参数是Flash视频，文件名后缀为.flv

    print("开始将字符型图片变为视频：")
    # 输出视频参数设置,包含视频文件名、编码器、帧率、视频宽高(此处参数需和字符图片大小一致)
    video_file = finalVideo_path + 'out' + '_' + 'ascci' + '_' + path
    videoWriter = cv2.VideoWriter(video_file, fourcc, 30.0,
                                  (asciiImage.width, asciiImage.height))
    # 循环读取图片
    for i in range(1, c):
        filename = ascii_path + str(i) + '.jpg'
        # 判断图片是否存在
        if os.path.exists(filename):
            img = cv2.imread(filename=filename)
            # 在一个给定的时间内(单位ms)等待用户按键触发,100ms
            cv2.waitKey(100)
            # 将图片写入视频中
            videoWriter.write(img)
            print(str(i) + '.jpg' + ' done!')
    # 视频释放
    videoWriter.release()
    print("字符视频已成功生成!!!")
    return video_file

def VideoToMp3(path, finalVideo_path):  # 分离原视频中的音乐
    outMusic_name = finalVideo_path + path.split('.')[0] + '.mp3'  # 将原视频文件后缀名去掉加上.mp3
    os.system(f"ffmpeg -i {path} -vn {outMusic_name} ")
    return outMusic_name

def VideoAddMp3(video_file, outMusic_name):  # 将分离出来的原视频中的音乐和字符视频合并
    video_final = finalVideo_path + 'Final' + '_' + '_' + path
    os.system(f"ffmpeg -i {outMusic_name} -i {video_file} {video_final}")

def VideoToPicture(path):
    # 进行视频的载入
    vc = cv2.VideoCapture(path)
    print("开始将原视频分割为图片：")
    c = 0
    # 判断载入的视频是否可以打开
    ret = vc.isOpened()
    # 循环读取视频帧
    while ret:
        c = c + 1
        # 进行单张图片的读取,ret的值为True或者Flase,frame表示读入的图片
        ret, frame = vc.read()
        if ret:
            # 存储为图像
            cv2.imwrite(folder_path + str(c) + '.jpg', frame)
            # 输出图像名称
            print(folder_path + str(c) + '.jpg')
            # 在一个给定的时间内(单位ms)等待用户按键触发,1ms
            cv2.waitKey(1)
        else:
            break
    # 视频释放
    vc.release()
    return c

def linkToVideo(link_url):
     print("======================================================================================================================\n")
     print("=============================================以下为例子，请参考===========================================================\n")
     print("https://youtu.be/_P4Bn_dWjqc\n"
           "请选择是否下载该视频 Y/N  : y\n"
           "[youtube] _P4Bn_dWjqc: Downloading webpage\n"
           "[info] Available formats for _P4Bn_dWjqc:\n"
           "format code  extension  resolution note\n"
           "249          webm       audio only tiny   50k , webm_dash container, opus @ 50k (48000Hz), 8.75MiB\n"
           "250          webm       audio only tiny   70k , webm_dash container, opus @ 70k (48000Hz), 12.11MiB\n"
           "140          m4a        audio only tiny  129k , m4a_dash container, mp4a.40.2@129k (44100Hz), 22.32MiB\n"
           "160          mp4        256x144    144p   70k , mp4_dash container, avc1.4d400c@  70k, 30fps, video only, 12.16MiB\n"
           "22           mp4        1280x720   720p  861k , avc1.64001F, 30fps, mp4a.40.2 (44100Hz) (best)\n"
           "请按’视频序号+音频序号‘顺序选择输入视频和音频组合，如果只有一个就只输入一个数字，例如：\n"
           "160+249\n"
           "[youtube] _P4Bn_dWjqc: Downloading webpage\n"
           "[download] Destination: 云计算是什么？下一代的计算机是什么样的？-_P4Bn_dWjqc.f160.mp4\n"
           "[download] 100% of 12.16MiB in 04:22   \n")
     print( "======================================================================================================================\n")
     print("==============================================例子结束==================================================================")

     os.system(f"youtube-dl -F {link_url}")
     print("====请按’视频序号+音频序号‘顺序选择输入视频和音频组合，如果只有一个就只输入一个数字===== ")
     VA = input()
     os.system(f"youtube-dl -f {VA} {link_url} -o VideoDownload.mp4")

if __name__ == '__main__':
    while True:
        print("Tips:视频下载功能可以下载Bilibili ,Youtube（需要全局代理）等网址视频，输入的网址格式不要携带多余的html信息，\n"
              "如要下载例如腾讯视频等网站的视频，请勿直接复制网址链接，请利用网页检查功能（F12）找到视频真正的网址，具体方法请百度")
        link_url = input("请输入视频网址例如（https://www.bilibili.com/video/BV1J4411v7g6/）\n")
        tag = input("请选择是否下载该视频 Y/N  : ")

        if tag == "Y" or tag == "y":
            linkToVideo(link_url)
            print("视频下载成功\n")

            while True:
                flag = input("请选择是否将下载的视频转为字符视频 Y/N  : \n")
                if flag == "Y" or flag == "y":
            # path = 'tt.mp4'
                    print("现在显示的是当前目录下的文件\n")
                    print(os.listdir('.'))  # 显示当前目录下文件，便于输入视频名称
                    path = input("请输入视频地址（例C://Users//Desktop//aa.mp4，如和本程序同一文件夹可直接输入文件名:\n")

            # 逐帧图片存储路径
                    folder_path = "imgbear/"
                    os.makedirs(folder_path)
                    print(f"已为您创建目录 <{folder_path}> ,该目录为视频分割出的逐帧图片输出目录")

            # 字符图片存储路径
                    ascii_path = 'imgout/'
                    os.makedirs(ascii_path)
                    print(f"已为您创建目录 <{ascii_path}> ,该目录为图片转化的字符图片存储目录")

            # 转化出的视频和音乐存储路径
                    finalVideo_path = 'finalVideo/'
                    os.makedirs(finalVideo_path)
                    print(f"已为您创建目录 <{finalVideo_path}> ,该目录为转化出的视频和音乐存储目录")

                    c = VideoToPicture(path)  # 视频分割成图片
                    outMusic_name = VideoToMp3(path, finalVideo_path)
                    asciiImage = PictureToChar(folder_path, ascii_path, c)  # 图片变成字符图片
                    video_file = charToVideo(ascii_path, asciiImage, path, c, finalVideo_path)  # 字符图片合成视频
                    VideoAddMp3(video_file, outMusic_name)
                    exit()

                elif flag == "N" or flag == "n":
                    print("你已退出了该程序！")
                    exit()
                else:
                     print("你输入的内容有误，请重输入！")

        elif tag == "N" or tag == "n":
           print("你已退出了该程序！")
           exit()
        else:
           print("你输入的内容有误，请重新输入！")
