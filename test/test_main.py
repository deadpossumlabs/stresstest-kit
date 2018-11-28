import unittest
from pprint import pprint

import inject

from block_inspector import BlockInspector
from conf import infura_config
from main import import_block
from mappers.transaction_mapper import TransactionMapper


class FunctionalTestCase(unittest.TestCase):

    def test_transfers(self):
        inject.configure(infura_config)
        inspector = BlockInspector()

        while True:
            block = inspector.get_next_block()
            if block is None:
                continue

            txs = import_block(block)

            for tx in txs:
                pprint(TransactionMapper.transaction_to_dict(tx))

            break


if __name__ == '__main__':
    unittest.main()
