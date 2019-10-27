# import libraries
from vidgear.gears import NetGear
import cv2





stream = cv2.VideoCapture(0) #Open any video stream
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 2560x1920 2217x2217 2952×1944 1920x1080
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
stream.set(cv2.CAP_PROP_FPS, 20)

options = {'flag' : 0, 'copy' : False, 'track' : False}

#change following IP address '192.168.x.xxx' with yours
server = NetGear(address = '172.20.10.7', port = '6767', protocol = 'udp',  pattern = 0, receive_mode = False, logging = True, **options) #Define netgear server at your system IP address.

# infinite loop until [Ctrl+C] is pressed
while True:
	try: 
		(grabbed, frame) = stream.read()
		# read frames

		# check if frame is not grabbed
		if not grabbed:
			#if True break the infinite loop
			break

		# do something with frame here

		# send frame to server
		server.send(frame)
	
	except KeyboardInterrupt:
		#break the infinite loop
		break

# safely close video stream
stream.release()
# safely close server
server.close()