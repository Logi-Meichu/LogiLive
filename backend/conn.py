import socket
import struct
import pickle
from threading import Thread

class ConnClient:

    def __init__(self, host='127.0.0.1', port=8125, logger=None):
        self.logger = logger
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.conn = self.client_socket.makefile('wb')
        self.op_counter = 0
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        self.logger.debug("payload_size: {}".format(self.payload_size))
        self.logger.debug('connect to {}:{}'.format(host, port))

    def __del__(self):
        if self.conn:
            print('close connection and socket!')
            self.conn.close()
            self.client_socket.close()

    def transmit(self, input_data):
        '''
        To transmit data to the server. This is blocking function call and will wait for server response.
        :param input_data: the data to transmit
        :return: ret_data: the data received (can use directly!)
        '''

        self.op_counter += 1
        self.logger.debug('Input data: {}'.format(self.op_counter, input_data))

        send_data_pickle = pickle.dumps(input_data, 0)
        size = len(send_data_pickle)

        self.logger.debug("Current send {}: {}".format(self.op_counter, size))
        self.client_socket.sendall(struct.pack(">L", size) + send_data_pickle)

        # Receive data
        while len(self.data) < self.payload_size:  # To read the length information
            self.logger.debug("Recv: {}".format(len(self.data)))
            self.data += self.client_socket.recv(4096)  # read more until length information arrived

        self.logger.debug("Done Recv: {}".format(len(self.data)))
        packed_msg_size = self.data[:self.payload_size]  # to get the length (header) part information
        self.data = self.data[self.payload_size:]  # leftovers are the images pickle
        msg_size = struct.unpack(">L", packed_msg_size)[0]  # to extract out the exact size info
        self.logger.debug("msg_size: {}".format(msg_size))

        while len(self.data) < msg_size:  # read until all data arrived
            self.data += self.client_socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]  # left for next packet!

        # Process according to server response
        self.logger.debug('Received response! size = {}'.format(len(frame_data)))
        ret_data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        return ret_data

    def close(self):
        if self.conn:
            print('close connection and socket!')
            self.conn.close()
            self.client_socket.close()

    def read(self):
        
        # Receive data
        while len(self.data) < self.payload_size:  # To read the length information
            self.logger.debug("Recv: {}".format(len(self.data)))
            self.data += self.client_socket.recv(4096)  # read more until length information arrived

        self.logger.debug("Done Recv: {}".format(len(self.data)))
        packed_msg_size = self.data[:self.payload_size]  # to get the length (header) part information
        self.data = self.data[self.payload_size:]  # leftovers are the images pickle
        msg_size = struct.unpack(">L", packed_msg_size)[0]  # to extract out the exact size info
        self.logger.debug("msg_size: {}".format(msg_size))

        while len(self.data) < msg_size:  # read until all data arrived
            self.data += self.client_socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]  # left for next packet!

        # Process according to server response
        self.logger.debug('Received response! size = {}'.format(len(frame_data)))
        ret_data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        return ret_data
        

class ConnServer:

    def __init__(self, host='127.0.0.1', port=8125, logger=None):
        self.logger = logger
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.logger.info('Socket created (address reuseable)')
        self.server_socket.bind((host, port))
        self.logger.info('Socket bind {}:{} complete'.format(host, port))
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        self.is_setup = False
        self.logger.info("payload_size: {}".format(self.payload_size))
        t = Thread(target=self.init_conn, args=())
        t.daemon = True
        t.start()
    
    def init_conn(self):
        self.server_socket.listen(10000)
        self.logger.info('Socket now listening')
        self.conn, addr = self.server_socket.accept()
        self.logger.info('Socket now has connection from {}'.format(addr))
        self.is_setup = True

    
        
    def __del__(self):
        self.conn.close()

    def read(self):
        while True:
            if self.is_setup:
                break

        # Receive data
        while len(self.data) < self.payload_size:  # To read the length information
            self.logger.info("Recv: {} | payload_size: {}".format(len(self.data), self.payload_size))
            self.data += self.conn.recv(4096)  # read more until length information arrived

        self.logger.info("Done Recv: {}".format(len(self.data)))

        packed_msg_size = self.data[:self.payload_size]  # to get the length (header) part information
        self.data = self.data[self.payload_size:]  # leftovers are the images pickle
        msg_size = struct.unpack(">L", packed_msg_size)[0]  # to extract out the exact size info
        self.logger.info("msg_size: {}".format(msg_size))

        while len(self.data) < msg_size:  # read until all data arrived
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]  # left for next packet!

        # Process according to server response
        self.logger.debug('Received request! size = {}'.format(len(frame_data)))
        ret_data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

        return ret_data

    def send(self, input_data):
        ret_data = pickle.dumps(input_data, 0)
        size = len(ret_data)
        self.logger.info('Current send: {}'.format(size))
        self.conn.sendall(struct.pack(">L", size) + ret_data)
        self.logger.info('Data sent')
