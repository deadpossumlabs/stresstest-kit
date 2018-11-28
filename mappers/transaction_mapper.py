from mappers.transfer_mapper import TransferMapper
from models.transaction import Transaction
from utils import hex_to_dec, to_normalized_address


class TransactionMapper(object):
    @classmethod
    def json_dict_to_transaction(self, json_dict):
        transaction = Transaction()
        transaction.hash = json_dict.get('hash', None)
        transaction.nonce = hex_to_dec(json_dict.get('nonce', None))
        transaction.block_hash = json_dict.get('blockHash', None)
        transaction.block_number = hex_to_dec(json_dict.get('blockNumber', None))
        transaction.transaction_index = hex_to_dec(json_dict.get('transactionIndex', None))
        transaction.from_address = to_normalized_address(json_dict.get('from', None))
        transaction.to_address = to_normalized_address(json_dict.get('to', None))
        transaction.value = hex_to_dec(json_dict.get('value', None))
        transaction.gas = hex_to_dec(json_dict.get('gas', None))
        transaction.gas_price = hex_to_dec(json_dict.get('gasPrice', None))
        transaction.input = json_dict.get('input', None)
        return transaction

    @classmethod
    def transaction_to_dict(self, transaction):
        obj = {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'block_number': transaction.block_number,
            'transaction_index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.value,
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'input': transaction.input,
            'totals': transaction.totals,
            'transfers': []
        }

        if len(transaction.transfers) > 0:
            for transfer in transaction.transfers:
                obj['transfers'].append(TransferMapper.transfer_to_dict(transfer))

        return obj
