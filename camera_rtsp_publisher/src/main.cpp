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

    bool isTransimitting = false;    

    //cap.open("config_files/sample_1080p_h264.mp4"); //打开相机        
    cap.open(0); //打开相机                

    if (!cap.isOpened()) //判断相机是否打开               
    {
        std::cerr << "ERROR!!Unable to open camera\n";
        return -1;
    }
    else
    {
        fps = int(cap.get(cv::CAP_PROP_FPS));
        width = int(cap.get(cv::CAP_PROP_FRAME_WIDTH));
        height = int(cap.get(cv::CAP_PROP_FRAME_HEIGHT));

        printf("width=%d,height=%d,fps=%d\n", width, height, fps);

        isTransimitting = true;
    }
    
    /*
    std::string rtsp_server_url = "rtsp://172.17.0.1:8554/rtsp_camera";

    command << "ffmpeg ";
    command << "-y "
            << "-v 24 "
            << "-f rawvideo "
            <<"-vcodec rawvideo "
            <<"-pix_fmt bgr24 "
            <<"-s "
            << width
            << "x"
            << height
            << " "
            << "-r "   //set frame rate (Hz value, fraction or abbreviation)
            << fps;

    command << " -i - "
            << "-c:v libx264 "
            << "-f rtsp "
            << rtsp_server_url;
    */

    std::string rtsp_server_url = "rtsp://172.17.0.1:8554/rtsp_camera";

    command << "ffmpeg ";
    command << "-y "
            << "-v 24 "
            << "-f rawvideo "
            <<"-vcodec rawvideo "
            <<"-pix_fmt bgr24 "
            <<"-s "
            << width
            << "x"
            << height
            << " "
            << "-r "
            << fps;

    command << " -i - "
            << "-vf format=nv12 "
            << "-c:v h264_nvenc "
            << "-preset fast "
            << "-f rtsp "
            << rtsp_server_url;


    /* RTMP
    std::string rtmp_server_url = "rtmp://192.168.8.136:1935/13988888888/0";

    std::stringstream command;
    command << "ffmpeg ";

    // infile options
    command << "-y "  // overwrite output files
        << "-an " // disable audio
        << "-f rawvideo " // force format to rawvideo
        << "-vcodec rawvideo "  // force video rawvideo ('copy' to copy stream)
        << "-pix_fmt bgr24 "  // set pixel format to bgr24
        << "-s "  // set frame size (WxH or abbreviation)
        << width
        << "x"
        << height
        << " "
        << "-r " // set frame rate (Hz value, fraction or abbreviation)
        << fps
        << " ";

    command << "-i - "; //

    // outfile options
    command << "-c:v libx264 "  // Hyper fast Audio and Video encoder
        << "-pix_fmt yuv420p "  // set pixel format to yuv420p
        << "-preset ultrafast " // set the libx264 encoding preset to ultrafast
        << "-f flv " // force format to flv
        << rtmp_server_url;
    */
 
    FILE *fp = nullptr;
    fp = popen(command.str().c_str(), "w");

    cv::Mat frame;

    if (fp != nullptr) 
    {
        while (isTransimitting)
        {
            cap >> frame; //以流形式捕获图像

            cv::namedWindow("rtsp_server_url", 1); //创建一个窗口用于显示图像，1代表窗口适应图像的分辨率进行拉伸。
            if (frame.empty() == false) //图像不为空则显示图像
            {
                cv::imshow("rtsp_server_url", frame);  
                
                try
                {
                    fwrite(frame.data, sizeof(char), frame.total() * frame.elemSize(), fp);
                }
                catch(std::exception& e)
                {
                    cout<<e.what()<<endl;
                }
            }
            
            int  key = cv::waitKey(30); //等待30ms
            if (key ==  int('q')) //按下q退出
            {
                break;
            }
        }

        pclose(fp);
        cap.release(); //释放相机捕获对象
        cv::destroyAllWindows(); //关闭所有窗口
    }    

    return 0;
}
