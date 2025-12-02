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
  
import cv2
import subprocess as sp
import queue
import threading
import time
 
# 打开摄像头
cap = cv2.VideoCapture(0)
 
# 设置输出视频的参数
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'h264')

#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
#out = cv2.VideoWriter('video_result.mp4', fourcc, 20.0, (640, 480))

#rtmpUrl = "rtsp://192.168.8.136:8554/stream"


fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("fps:" + str(fps) + ",width:" + str(width) + ":height=" + str(height))


#rtmpUrl = "rtsp://192.168.8.136:8554/stream"
rtmpUrl = "rtmp://192.168.8.136:1935/live/test"

"""
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


#ffmpeg -f dshow -i video="Integrated Camera" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -rtsp_transport udp -f rtsp rtsp://192.168.8.136/stream


p = sp.Popen(command, stdin=sp.PIPE)

COUNT = 0
 
while True:
    # 读取视频帧
    ret, frame = cap.read()
 
    # 处理视频帧
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # 显示视频帧
    cv2.imshow('frame', frame)

    #COUNT = COUNT + 1

    # 把每一帧图像保存成jpg格式（这一行可以根据需要选择保留）
    #cv2.imwrite('picture'+str(COUNT) + '.jpg', frame)
 
    # 将视频帧写入输出视频
    # out.write(frame)

    p.stdin.write(frame.tobytes())
 
    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #time.sleep(1/20)
 
# 释放资源
cap.release()
#out.release()
cv2.destroyAllWindows()
