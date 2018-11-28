from models.receipt_log import ReceiptLog
from utils import hex_to_dec


class TxReceiptLogMapper(object):

    def json_dict_to_receipt_log(self, json_dict):
        receipt_log = ReceiptLog()

        receipt_log.log_index = hex_to_dec(json_dict.get('logIndex', None))
        receipt_log.transaction_hash = json_dict.get('transactionHash', None)
        receipt_log.transaction_index = hex_to_dec(json_dict.get('transactionIndex', None))
        receipt_log.block_hash = json_dict.get('blockHash', None)
        receipt_log.block_number = hex_to_dec(json_dict.get('blockNumber', None))
        receipt_log.address = json_dict.get('address', None)
        receipt_log.data = json_dict.get('data', None)
        receipt_log.topics = json_dict.get('topics', None)

        return receipt_log

    def web3_dict_to_receipt_log(self, dict):

        receipt_log = ReceiptLog()

        receipt_log.log_index = dict.get('logIndex', None)

        transaction_hash = dict.get('transactionHash', None)
        if transaction_hash is not None:
            transaction_hash = transaction_hash.hex()
        receipt_log.transaction_hash = transaction_hash

        block_hash = dict.get('blockHash', None)
        if block_hash is not None:
            block_hash = block_hash.hex()
        receipt_log.block_hash = block_hash

        receipt_log.block_number = dict.get('blockNumber', None)
        receipt_log.address = dict.get('address', None)
        receipt_log.data = dict.get('data', None)

        if 'topics' in dict:
            receipt_log.topics = [topic.hex() for topic in dict['topics']]

        return receipt_log

    def receipt_log_to_dict(self, receipt_log):
        return {
            'type': 'log',
            'log_index': receipt_log.log_index,
            'transaction_hash': receipt_log.transaction_hash,
            'transaction_index': receipt_log.transaction_index,
            'block_hash': receipt_log.block_hash,
            'block_number': receipt_log.block_number,
            'address': receipt_log.address,
            'data': receipt_log.data,
            'topics': receipt_log.topics
        }

    def dict_to_receipt_log(self, dict):
        receipt_log = ReceiptLog()

        receipt_log.log_index = dict.get('log_index')
        receipt_log.transaction_hash = dict.get('transaction_hash')
        receipt_log.transaction_index = dict.get('transaction_index')
        receipt_log.block_hash = dict.get('block_hash')
        receipt_log.block_number = dict.get('block_number')
        receipt_log.address = dict.get('address')
        receipt_log.data = dict.get('data')

        topics = dict.get('topics')
        if isinstance(topics, str):
            if len(topics.strip()) == 0:
                receipt_log.topics = []
            else:
                receipt_log.topics = topics.strip().split(',')
        else:
            receipt_log.topics = topics

        return receipt_log
