import logging
import time

import inject
from eth_rpc_api import ParityEthJsonRpc

from models.transaction import Transaction
from utils import hex_to_dec


def singleton(cls):
    instances = {}

    def getinstance(*args):
        if cls not in instances:
            instances[cls] = cls(*args)
        return instances[cls]

    return getinstance


# @singleton
class BlockInspector(object):
    rpc_client = inject.attr(ParityEthJsonRpc)
    current_block = 0

    def __init__(self):
        self.current_block = 100100
        self.logger = logging.getLogger()

    def get_prev_block(self) -> Transaction:
        return self.__get_another_block(-1)

    def __get_another_block(self, step: int):
        # logger.error(e, exc_info=True, extra={"txid": transaction['hash']})

        while True:
            print("\tReading {0} block".format(self.current_block))
            block = self.rpc_client.eth_getBlockByNumber(self.current_block)

            if block is None:
                time.sleep(1)
                self.logger.info("Sleeping on ", extra={"number": self.current_block})
                continue

            self.current_block = hex_to_dec(block['number']) + step
            self.logger.info("\tFetched new block", extra={"number": self.current_block - 1})

            return block

    def get_next_block(self) -> Transaction:
        return self.__get_another_block(1)

    def get_block(self, block_num: int):
        block = self.rpc_client.eth_getBlockByNumber(block_num)
        if block is None:
            self.logger.info("Block {0} not found".format(block_num))
        return block

    def get_last_block(self):
        self.rpc_client.eth_getBlockByNumber()
