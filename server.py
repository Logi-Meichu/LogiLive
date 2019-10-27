
from common import setup_logger
from conn import ConnServer


def run():
    
    while True:
        input_data = conn.read()
        # Process data from the request from client.
        logger.info('Operation received! start to process.')
        ret_data = process(input_data)
        conn.send(ret_data)
    

if __name__ = '__main__':
    logger = setup_logger()
    conn = ConnServer(host='127.0.0.1', port=8125, logger=logger)

    run()