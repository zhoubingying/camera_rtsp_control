
import cv2

def videocapture():
    cap=cv2.VideoCapture(0)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    #fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    #print(str(fourcc))
    
    #width = 1920
    #height = 1080
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 10

    writer = cv2.VideoWriter("video_1.mp4", fourcc, fps, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('testwell', frame)
        writer.write(frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    writer.release()
    cap.release()

if __name__ == '__main__' :
    videocapture()
