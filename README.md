# Python
#####  python_VideoDownload  #####
# 程序指南：本程序使用open CV2 ,os ,youtube_dl ,PIL等模块,需要自行导入,同时本程序运行的目录中需要有 /tool/ffmpeg.exe ,
#            使用视频转字符功能时，需要先删除 /finalVideo ,/imgbear , /imgout3个文件夹，以免发生冲突
# 程序功能：可以通过输入视频真实链接直接下载，已知支持的网站有Bilibili , Youtube等 ,可以自行摸索,须知是真实视频链接,并非直接在浏览器输入栏获取的链接,
#         部分网站可以通过网页检查（F12）方式自行获得
# 模块安装命令：pip install os
#              pip install pillow
#              pip install opencv-python
#              pip install youtube_dl
