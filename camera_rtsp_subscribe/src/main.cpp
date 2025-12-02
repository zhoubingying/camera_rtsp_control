#include <fstream>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    cv::VideoCapture cap;   //声明相机捕获对象
    int width, height, fps;
    std::stringstream command;

    int deviceID = 0; //相机设备号

    bool isTransimitting = true;

    //std::string rtsp_server_url = "rtsp://172.17.0.1:8554/rtsp_camera";
    std::string rtsp_server_url = "rtsp://192.168.3.106:8554/rtsp_camera";
    
    cap.open(rtsp_server_url); //打开相机

    fps = int(cap.get(cv::CAP_PROP_FPS));
    width = int(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    height = int(cap.get(cv::CAP_PROP_FRAME_HEIGHT));

    printf("width=%d,height=%d,fps=%d\n", width, height, fps);


    if (!cap.isOpened()) //判断相机是否打开
    {
        std::cerr << "ERROR!!Unable to open camera\n";
        return -1;
    }

    cv::Mat frame;
 
    while (isTransimitting)
    {
        cap >> frame; //以流形式捕获图像

        cv::namedWindow(rtsp_server_url, 1); //创建一个窗口用于显示图像，1代表窗口适应图像的分辨率进行拉伸。
        if (frame.empty() == false) //图像不为空则显示图像
        {
            cv::imshow(rtsp_server_url, frame);           
        }
        
        int  key = cv::waitKey(30); //等待30ms
        if (key ==  int('q')) //按下q退出
        {
            break;
        }
    }

    cap.release(); //释放相机捕获对象
    cv::destroyAllWindows(); //关闭所有窗口   
    

    return 0;
}
