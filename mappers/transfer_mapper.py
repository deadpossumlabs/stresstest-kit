from models.value_transfer import ValueTransfer


class TransferMapper(object):

    @classmethod
    def transfer_to_dict(cls, transfer):
        return {
            'value_id': transfer.value_id,
            'from_address': transfer.from_address,
            'to_address': transfer.to_address,
            'value': transfer.value,
            'transaction_hash': transfer.transaction_hash,
            'block_number': transfer.block_number,
        }

    @classmethod
    def json_to_transfer(cls, transfer):
        tr = ValueTransfer()
        tr.from_address = transfer['from_address']
        tr.to_address = transfer['to_address']
        tr.value = transfer['value']
        tr.value_id = transfer['value_id']
        tr.transaction_hash = transfer['transaction_hash']
        return tr
