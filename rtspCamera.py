"""
import cv2

def videocapture():
    cap=cv2.VideoCapture(0)
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #fps = cap.get(cv2.CAP_PROP_FPS)
    
    width = 640
    height = 480
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20
    #fourcc = cv2.VideoWriter_fourcc(*'h264')

    writer = cv2.VideoWriter("video_result.mp4", fourcc, fps, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('testwell', frame)
        writer.write(frame) 
    cap.release()

if __name__ == '__main__' :
  videocapture()
"""

# scp capture.py zhoubingying@192.168.8.136:/home/zhoubingying/video

  
import cv2
import subprocess as sp
import queue
import threading
import time
import os
 
# 打开摄像头
cap = cv2.VideoCapture(0)

#cap = cv2.VideoCapture('./video_result.mp4')


fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("fps:" + str(fps) + ",width:" + str(width) + ":height=" + str(height))
 
# 设置输出视频的参数
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'h264')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
#out = cv2.VideoWriter('video_result.mp4', fourcc, 20.0, (640, 480))

rtspUrl = "rtsp://172.17.0.1:8554/rtsp_camera"

"""
command = ['ffmpeg',
        '-y',
        '-v', '24',  # 日志显示等级
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-f', 'rtsp',
        #'-rtsp_transport', 'tcp',
        rtspUrl]
"""

command = ['ffmpeg',
        '-y',
        '-v', '24',  # 日志显示等级
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', "fast",
        '-f', 'rtsp',
        #'-rtsp_transport', 'tcp',
        rtspUrl]

# 使用指定的GPU索引
my_env = os.environ.copy()
my_env["CUDA_VISIBLE_DEVICES"] = 6

"""
rtmpUrl = "rtsp://192.168.8.136:554/stream"
#ffplay rtsp://192.168.8.136:554/stream
command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-f', 'rtsp',
        rtmpUrl]
"""

"""
#rtmpUrl = "rtmp://192.168.8.136:1935/live/test"
#ffplay rtmp://192.168.8.136:1935/live/test

command = ['ffmpeg',
                '-y',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', "{}x{}".format(width, height),
                '-r', str(fps),
                '-i', '-',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'ultrafast',
                '-f', 'flv',
                rtmpUrl]
"""


#ffmpeg -f rawvideo -i video="video0" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -rtsp_transport udp -f rtsp rtsp://192.168.8.136/stream


#pipe = sp.Popen(command, stdin=sp.PIPE, env=my_env)
pipe = sp.Popen(command, stdin=sp.PIPE)
num = 0

COUNT = 0
 
while True:
    num += 1

    """
    if pipe.poll() is not None:
        time.sleep(3)
        print(pipe.poll())
        #print("the popen of ffmpeg not run, restart this:%s" % self.name)
        #pipe = sp.Popen(command, stdin=sp.PIPE, env=my_env)
        pipe = sp.Popen(command, stdin=sp.PIPE)
    """

    # 读取视频帧
    ret, frame = cap.read()
 
    # 处理视频帧

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # 显示视频帧
    # cv2.imshow('frame', frame)

    #COUNT = COUNT + 1

    # 把每一帧图像保存成jpg格式（这一行可以根据需要选择保留）
    #cv2.imwrite('picture'+str(COUNT) + '.jpg', frame)
 
    # 将视频帧写入输出视频
    # out.write(frame)

    if num == 100:
        print("start sleep 50")
        time.sleep(50)
        print("end sleep 50")
    if num >= 100:
        print("超时后的，第%d次写入" % (num-99))
        time.sleep(5)

    try:
        pipe.stdin.write(frame.tobytes())  #存入管道用于直播
        num = 0
    except BrokenPipeError:
        print("Pushing the camera of %s appear ERROR:%s" % ('rtsp', rtspUrl))
        #print(traceback.format_exc())
    
 
    # 按 'q' 键退出循环
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

    #time.sleep(1/20)
 
# 释放资源
cap.release()
#out.release()
pipe.stdin.close()  # 关闭输入管道
pipe.communicate()  # 等待子进程关闭
cv2.destroyAllWindows()
