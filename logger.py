import logging, os
import time
logging.basicConfig(level=logging.NOTSET)
logging.debug("debug msg")
logging.info("info msg")
logging.warning("warning msg")
logging.error("error msg")
logging.critical("critical msg")

#cree a logger
# logger = logging.getLogger('__default_logger__')
# logger.setLevel(logging.INFO)
# #create a handler
# log_path = os.getcwd() + '/Logs/'
# log_name = log_path + '0128.log'
# log_file = log_name
# fh = logging.FileHandler(log_file, mode='w')
# fh.setLevel(logging.DEBUG)
#
# #define handler's format
# logformat = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(logformat)
# #add the logger to the handler
# logger.addHandler(fh)
#
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message...')