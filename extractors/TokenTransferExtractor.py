from logging import getLogger

import inject
from eth_rpc_api import ParityEthJsonRpc

from mappers.receipt_log_mapper import TxReceiptLogMapper
from models.transaction import Transaction
from models.value_transfer import TokenTransfer
from utils import split_to_words, to_normalized_address, word_to_address, hex_to_dec

TRANSFER_EVENT_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
logger = getLogger(__name__)


class TokenTransferExtractor(object):

    @classmethod
    def extract(self, tx: Transaction):
        cl = inject.instance(ParityEthJsonRpc)

        tx._reciept = cl.eth_getTransactionReceipt(tx.hash)

        mapper = TxReceiptLogMapper()

        for log_dict in tx._reciept['logs']:
            receipt_log = mapper.dict_to_receipt_log(log_dict)

            topics = receipt_log.topics
            if topics is None or len(topics) < 1:
                logger.warning("Topics are empty in log {} of transaction {}".format(receipt_log.log_index,
                                                                                     receipt_log.transaction_hash))
                continue

            if topics[0] == TRANSFER_EVENT_TOPIC:
                topics_with_data = topics + split_to_words(receipt_log.data)
                if len(topics_with_data) != 4:
                    logger.warning("The number of topics and data parts is not equal to 4 in log {} of transaction {}"
                                   .format(receipt_log.log_index, receipt_log.transaction_hash))
                    continue

                token_transfer = TokenTransfer()
                token_transfer.value_id = to_normalized_address(receipt_log.address)
                token_transfer.from_address = word_to_address(topics_with_data[1])
                token_transfer.to_address = word_to_address(topics_with_data[2])
                token_transfer.value = hex_to_dec(topics_with_data[3])
                token_transfer.transaction_hash = receipt_log.transaction_hash
                token_transfer.block_number = tx.block_number
                token_transfer.transaction_hash = tx.hash

                yield token_transfer
