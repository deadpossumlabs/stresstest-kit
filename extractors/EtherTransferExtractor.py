import inject
from eth_rpc_api import ParityEthJsonRpc

from models.transaction import Transaction
from models.value_transfer import EtherTransfer
from utils import hex_to_dec


class EtherTransferExtractor(object):

    @classmethod
    def extract_call(cls, trace_entry):
        transfer = EtherTransfer()
        transfer.from_address = trace_entry['action']['from']
        transfer.value = hex_to_dec(trace_entry['action']['value'])
        transfer.to_address = trace_entry['action']['to']

        return transfer

    @classmethod
    def extract_suicide(cls, trace_entry):
        transfer = EtherTransfer()
        transfer.value = hex_to_dec(trace_entry['action']['balance'])
        transfer.to_address = trace_entry['action']['refundAddress']
        transfer.from_address = trace_entry['action']['address']

        return transfer

    @classmethod
    def extract_create(cls, trace_entry):
        transfer = EtherTransfer()
        transfer.value = hex_to_dec(trace_entry['action']['value'])
        transfer.to_address = trace_entry['result']['address']
        transfer.from_address = trace_entry['action']['from']

        return transfer

    @classmethod
    def extract(cls, tx: Transaction):
        handlers = {
            "suicide": cls.extract_suicide,
            "create": cls.extract_create,
            "call": cls.extract_call
        }

        cl = inject.instance(ParityEthJsonRpc)

        tx._traces = cl.trace_transaction(tx.hash)

        for trace_entry in tx._traces:
            try:
                transfer = handlers[trace_entry['type']](trace_entry)

                if transfer.value > 0:
                    transfer.transaction_hash = tx.hash
                    transfer.block_number = tx.block_number

                    yield transfer
            except KeyError:
                print(tx.hash)
