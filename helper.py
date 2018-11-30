import json
import logging
import time

from hexbytes import HexBytes

# logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG) # bacic config
# logging.basicConfig(format = '%(levelname)-10s[%(asctime)s] %(message)s', level = logging.DEBUG, file = './logs/LOG-{1}-test{0}.log'.format(test_num, get_time())) # light config

FOLDERS = {
    "logs": "./logs/",
    "contracts": "./contracts/",
    "abi": "./contracts/abi/"
}


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def get_time():
    date = time.strptime(time.asctime())
    return "{0}.{1}.{2}[{3}:{4}:{5}]".format(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour,
                                             "0" + str(date.tm_min) if date.tm_min < 10 else date.tm_min,
                                             "0" + str(date.tm_sec) if date.tm_sec < 10 else date.tm_sec)


def get_logger(test_num):
    logger = logging.getLogger(str(test_num))
    logger.setLevel(logging.INFO)  # By default, logs all messages

    ch = logging.StreamHandler()  # StreamHandler logs to console
    ch.setLevel(logging.INFO)
    ch_format = logging.Formatter('%(levelname)-10s[%(asctime)s] %(message)s')
    ch.setFormatter(ch_format)

    fh = logging.FileHandler('./logs/LOG-{1}-test{0}.log'.format(test_num, get_time()))
    fh.setLevel(logging.INFO)
    fh_format = logging.Formatter('%(levelname)-10s[%(asctime)s] %(message)s')
    fh.setFormatter(fh_format)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

