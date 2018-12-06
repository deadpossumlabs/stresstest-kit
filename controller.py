import inject

from web3 import Web3
from block_inspector import BlockInspector
from threading import Thread
from helper import get_logger
from tests import Tests
from time import sleep


class TestController(object):

    __test_list = []

    def __new__(cls, host, config, accounts):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestController, cls).__new__(cls)
            inject.configure(config)
        return cls.instance

    def __init__(self, host, config, accounts):

        self.accounts = accounts
        self.setSprite = set()
        etherscan_provider = Web3.HTTPProvider(host, request_kwargs={'timeout': 30})
        self.__w3 = Web3(etherscan_provider)
        self.__inspector = BlockInspector()

    def get_list_test(self):
        return self.__test_list

    def add_test(self, func, args=list(), flows=1):
        self.__test_list.append({"func": func, "args": list(args), "flows": flows})

    def start_tests(self):
        test_num = 1
        for test in self.__test_list:
            logger = get_logger(test_num)
            list_flows = []
            test_obj = Tests(self.__w3, logger, self.__inspector)
            try:
                func_args = test["args"]

                if test_obj.is_thread(test["func"]):
                    list_flows = []
                    flows = test["flows"]
                    if flows > len(self.accounts):
                        flows = len(self.accounts)

                    for i in range(flows):
                        j = i + 1
                        if j == len(self.accounts):
                            j = 0
                        accounts = (self.accounts[i][0], self.accounts[i][1],
                                    self.accounts[j][0], self.accounts[j][1])
                        func_args.insert(0, accounts)
                        list_flows.append(Thread(target=test_obj.start_test, args=(test["func"], func_args.copy())))
                        func_args.pop(0)
                else:
                    list_flows.append(Thread(target=test_obj.start_test, args=(test["func"], func_args.copy())))

                logger.info("Start test {0}(flows: {3}): {1}{2}".format(test_num, test["func"],
                                                                        test["args"], len(list_flows)))

                for flow in list_flows:
                    flow.start()
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
