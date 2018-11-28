import inject

from web3 import Web3
from block_inspector import BlockInspector
from threading import Thread
from helper import get_logger
from tests import Tests


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
        etherscan_provider = Web3.HTTPProvider(host)
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
                # if type(func_args) is not tuple and type(func_args) is not list:
                #     func_args = tuple(func_args)
                if test["accounts"]:
                    for i in range(len(test["accounts"])):
                        args = func_args.copy()
                        print(args)
                        flows += 1
                        j = i + 1
                        if i == len(test["accounts"]) - 1:
                            j = -1
                        accounts = (test["accounts"][i][0], test["accounts"][i][1],
                                    test["accounts"][j][0], test["accounts"][j][1])
                        args.append(accounts)
                        print(args)
                        list_args.append(args)
                else:
                    list_args.append(func_args)
                    flows += 1
                logger.info("Start test {0}(flows: {3}): {1}{2}".format(test_num, test["func"],
                                                                       test["args"], flows))
                # if test["accounts"]:
                #     for i in range(len(test["accounts"])):
                #         j = i + 1
                #         if i == len(test["accounts"]) - 1:
                #             j = -1
                #         accounts = (test["accounts"][i][0], test["accounts"][i][1],
                #                     test["accounts"][j][0], test["accounts"][j][1])
                #         list_flows.append(Thread(target=test_obj.start_test, args=(test["func"], accounts)))
                #         list_flows[-1].start()
                # else:
                for i in range(flows):
                        # if len(test["args"]) == 0:
                        #     self.__logger.info("Start test {0}: {1}()".format(test_num, test["func"], test["args"]))
                        #     list_flows.append(Thread(target=test_obj.start_test, args=(test["func"],)))
                        # else:
                        # args = []
                        # args = [self.__w3, self.__logger, self.__inspector]
                        # if test["time"] is not None:
                        #     args.append(test["time"])

                        # if len(func_args) > 1:
                        #     args.extend(func_args)
                        # elif len(func_args) is 1:
                        #     args.append(*func_args)

                        # list_flows.append(Thread(target=test["func"], args=func_args))
                    list_flows.append(Thread(target=test_obj.start_test, args=(test["func"], list_args[i])))
                    list_flows[-1].start()
                while True:
                    list_alive = [state.is_alive() for state in list_flows if state.is_alive()]
                    if not list_alive:
                        break

            except TypeError as e:
                logger.error("\tUnhandled error in cycle:{0}{1}".format(e.__class__.__name__, e))

                continue

            finally:
                test_num += 1
