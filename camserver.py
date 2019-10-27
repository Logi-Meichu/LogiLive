# import libraries
import cv2
import numpy as np
import face_recognition
from threading import Thread
from vidgear.gears import NetGear
from conn import ConnServer
from common import setup_logger



class LogitechLive:
    
    def __init__(self):
        print('Initializes')
        options = {'flag' : 0, 'copy' : False, 'track' : False}
        # options = {'multiserver_mode': True}

        # self.client = #activate multiserver_mode
        #Change the Client with your system IP address and port address of each unique Server((5566,5567) in our case), plus activate pattern Pub/Sub(`2`), `recieve_mode`, and `logging` for debugging
        # self.client = NetGear(address = '127.0.0.1', port = (6767,6768), protocol = 'tcp', pattern = 2, receive_mode = True, **options) 
        # self.client = NetGear(address = '192.168.0.1', port = (5566,5567), protocol = 'tcp', pattern = 2, receive_mode = True, **options) 

        self.motor_conn = ConnServer(host='172.20.10.7', port=8202, logger=logger)
        self.pad_conn = ConnServer(host='172.20.10.7', port=8300, logger=logger)

        self.camera1_conn = ConnServer(host='172.20.10.7', port=9302, logger=logger)
        self.camera2_conn = ConnServer(host='172.20.10.7', port=9300, logger=logger)

        self.clients = {
            '172.20.10.2': NetGear(address = '172.20.10.7', port = '6768', protocol = 'tcp',  pattern = 0, receive_mode = True, logging = True, **options),
            '172.20.10.13': NetGear(address = '172.20.10.7', port = '6767', protocol = 'tcp',  pattern = 0, receive_mode = True, logging = True, **options)
        }

        self.ip_dict = {
            '172.20.10.2': {
                'conn': False,
                'face': False,
                'port': 8201,
            }, 
            '172.20.10.13': {
                'conn': True,
                'face': True,
                'port': 8202,
            }
        }
        self.frame_dict = {}

        self.mode = 'dev'
        # Control Tools
        self.main_stream = '172.20.10.2'
        self.stopped = False
    
    def start(self):
        print('start thread')
        for ip in self.ip_dict.keys():
            t = Thread(target=self.update, args=(ip, ))
            t.daemon = True
            t.start()
        print('starting control command listener')
        t = Thread(target=self.control_listener, args=())
        t.daemon = True
        t.start()
        return self

    def face_recognition(self, frame):
        print('run face detection')
        # Resize frame of video to 1/4 size for faster face detection processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame, model="cnn")

        # Display the results
        for top, right, bottom, left in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame,(left,bottom),(right,top),(0,255,0),2)

            # Run face detection
            print('end face detection; send data {}, {}'.format((left+right)//2, (top+bottom)//2))
            send_data = {
                'x': (left+right)//2,
                'y': (top+bottom)//2
            }
            
            self.motor_conn.send(send_data)

            # We only care of the most prominent person
            break

    def update(self, ip):
        print('Reading {}'.format(ip))

        # infinite loop
        while True:
            print('receive a frame ({})'.format(ip))
            frame = self.clients[ip].recv()
            if frame is None:
                continue

            # Face detection
            if self.ip_dict[ip]['face']:
                t = Thread(target=self.face_recognition, args=(frame, ))
                t.daemon = True
                t.start()

            self.frame_dict[ip] = frame
            print('address {} received.'.format(ip))

            print('send frame to host.')
            if ip == '172.20.10.13':
                self.camera1_conn.send(frame)
            elif ip == '172.20.10.2':
                self.camera2_conn.send(frame)
        
        print('finish camera fetching thread! {}'.format(ip))

    def control_listener(self):
        while True:
            data = self.pad_conn.read()
            # Process data from the request from client.
            logger.info('Operation received! start to process.')
            logger.info(data)
            # Process received data

            if data['method'] == 'switch':
                self.main_stream = data['value']
            elif data['method'] == 'stop':
                self.stopped = True
            elif data['method'] == 'start':
                self.stopped = False
            elif data['method'] == 'screenshot':
                pass

            self.pad_conn.send({'status': 'success'})

    def display(self):
        print('start display')
        while True:
            image = None
            if self.mode == 'dev':
                frame_list = []
                for key, value in self.frame_dict.items():
                    frame_list.append(value)
                
                if not len(frame_list):
                    continue
                image = np.hstack(frame_list)
            elif self.mode == 'production':
                image = self.frame_dict.get(self.main_stream)

            if image is None:
                continue

            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.imshow("image", image)

            if cv2.waitKey(1) & 0xFF == ord('p'):
                self.mode = 'production'
            elif cv2.waitKey(1) & 0xFF == ord('d'):
                self.mode = 'dev'
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    def __del__(self):
        cv2.destroyAllWindows()
        # safely close client
        # self.clients[1].close()
        # clients[1].close()

if __name__ == '__main__':
    logger = setup_logger()
    cam = LogitechLive().start()
    cam.display()