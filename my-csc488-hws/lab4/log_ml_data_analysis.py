import logging
import socket
format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(lineno)s - %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=format_str)    # configs the logging instance

