import inject

from web3 import Web3
from block_inspector import BlockInspector
from threading import Thread
from helper import get_logger
from tests import Tests
from time import sleep


class TestController(object):

    __test_list = []
    __params = []

    def __new__(cls, host, config):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestController, cls).__new__(cls)
            inject.configure(config)
        return cls.instance

    def __init__(self, host, config):

        self.setSprite = set()
        etherscan_provider = Web3.HTTPProvider(host, request_kwargs={'timeout': 30})
        self.__w3 = Web3(etherscan_provider)
        self.__inspector = BlockInspector()

    def get_list_test(self):
        return self.__test_list

    def get_params(self):
        return self.__params

    def add_test(self, func, args=tuple(), accounts=None):
        self.__test_list.append({"func": func, "args": args, "accounts": accounts})

    def start_tests(self):
        test_num = 1
        for test in self.__test_list:
            flows = 0
            logger = get_logger(test_num)
            list_flows = []
            test_obj = Tests(self.__w3, logger, self.__inspector)
            try:
                list_args = []
                func_args = list(test["args"])

                if test["accounts"]:
                    for i in range(len(test["accounts"])):
                        j = i + 1
                        if j == len(test["accounts"]):
                            j = 0
                        args = func_args.copy()
                        flows += 1

                        accounts = (test["accounts"][i][0], test["accounts"][i][1],
                                    test["accounts"][j][0], test["accounts"][j][1])
                        args.insert(0, accounts)
                        list_args.append(args)
                else:
                    list_args.append(func_args)
                    flows += 1
                logger.info("Start test {0}(flows: {3}): {1}{2}".format(test_num, test["func"],
                                                                        test["args"], flows))

                for i in range(flows):

                    list_flows.append(Thread(target=test_obj.start_test, args=(test["func"], list_args[i])))
                    list_flows[-1].start()
                while True:
                    list_alive = [state.is_alive() for state in list_flows if state.is_alive()]
                    if not list_alive:
                        break

            except TypeError as e:
                logger.error("\tUnhandled error in starting {2}:{0}{1}".format(e.__class__.__name__, e, test["func"]))

                continue

            finally:
                test_num += 1
                sleep(5)  # There are cases when transactions in same tests do not have time to process on the node
