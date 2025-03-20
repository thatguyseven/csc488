import logging
import socket
format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(lineno)s - %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=format_str)    # configs the logging instance

logging.debug('This is a DEBUG message')
logging.info('This is a INFO message')
logging.warning('This is a WARNING message')
logging.error('This is a ERROR message')
logging.critical('This is a CRITICAL message')
