import cv2
import subprocess
 
# rtsp = "rtsp://admin:a12345678@10.10.8.101:554/h264/ch1/main/av_stream"
# rtmp = 
rtmp = ''
 
# 读取视频并获取属性
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("./IMG_4438.mov")
cap.set(3, 640)
cap.set(4, 480)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 2560x1920 2217x2217 2952×1944 1920x1080
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 20)

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
sizeStr = str(size[0]) + 'x' + str(size[1])
fps = cap.get(cv2.CAP_PROP_FPS)  # 30p/self
fps = int(fps)
 
hz = int(1000.0 / fps)
print('size:' + sizeStr + ' fps:' + str(fps) + ' hz:' + str(hz))

# rtmp://a.rtmp.youtube.com/live2/a3fu-28r7-zxg5-emer

rtmp = 'rtmp://localhost:1935/rtmp/room'




command = ['ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv', 
    rtmp]


# command = ['ffmpeg',
#     '-y',
#     '-f', 'rawvideo',
#     '-vcodec','rawvideo',
#     '-pix_fmt', 'bgr24',
#     '-s', sizeStr,
#     '-i', '-',
#     '-c:v', 'libx264',
#     '-pix_fmt', 'yuv420p',
#     '-preset', 'ultrafast',
#     '-f', 'flv',
#     rtmp]

# ffmpeg \
#     -i "$SOURCE" -deinterlace \
#     -vcodec libx264 -pix_fmt yuv420p -preset $QUAL -r $FPS -g $(($FPS * 2)) -b:v $VBR \
#     -acodec libmp3lame -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k \
#     -f flv "$YOUTUBE_URL/$KEY"

# command = ['ffmpeg',
#     '-y', '-an',
#     '-f', 'rawvideo',
#     '-vcodec','rawvideo',
#     '-pix_fmt', 'bgr24',
#     '-s', sizeStr,
#     '-r', '25',
#     '-i', '-',
#     '-c:v', 'libx264',
#     '-pix_fmt', 'yuv420p',
#     '-preset', 'ultrafast',
#     '-f', 'flv',
#     rtmp]
 
pipe = subprocess.Popen(command
    , shell=False
    , stdin=subprocess.PIPE
)
 
while cap.isOpened():
    success,frame = cap.read()
    if success:
        '''
		对frame进行识别处理
		'''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
        pipe.stdin.write(frame.tostring())
 
cap.release()
pipe.terminate()