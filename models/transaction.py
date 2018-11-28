from models.value_transfer import ValueTransfer


class Transaction(object):
    def __init__(self):
        self.hash = None
        self.nonce = None
        self.block_hash = None
        self.block_number = None
        self.transaction_index = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.gas = None
        self.gas_price = None
        self.input = None
        self.totals = {}
        self.transfers = []

        self._receipt = {}
        self._traces = {}

    def add_transfer(self, transfer: ValueTransfer):
        self.transfers.append(transfer)

        if transfer.from_address in self.totals:
            if transfer.value_id in self.totals[transfer.from_address]:
                self.totals[transfer.from_address][transfer.value_id]["sent"] += transfer.value
                if self.totals[transfer.from_address][transfer.value_id]['to'] is not None and \
                        self.totals[transfer.from_address][transfer.value_id]['to'] != transfer.to_address:
                    self.totals[transfer.from_address][transfer.value_id]['to'] = "MORE THAN ONE RECEIVER"
                else:
                    self.totals[transfer.from_address][transfer.value_id]['to'] = transfer.to_address
            else:
                self.totals[transfer.from_address][transfer.value_id] = {"sent": transfer.value,
                                                                         'to': transfer.to_address, 'from': None,
                                                                         "received": 0}

        else:
            self.totals[transfer.from_address] = {
                transfer.value_id: {"sent": transfer.value, "from": None, 'to': transfer.to_address, "received": 0}}

        if transfer.to_address in self.totals:
            if transfer.value_id in self.totals[transfer.to_address]:
                self.totals[transfer.to_address][transfer.value_id]["received"] += transfer.value
                if self.totals[transfer.to_address][transfer.value_id]['from'] is not None and \
                        self.totals[transfer.to_address][transfer.value_id]['from'] != transfer.to_address:
                    self.totals[transfer.to_address][transfer.value_id]['from'] = "MORE THAN ONE SENDER"
                else:
                    self.totals[transfer.to_address][transfer.value_id]['from'] = transfer.from_address
            else:
                self.totals[transfer.to_address][transfer.value_id] = {"sent": 0, "received": transfer.value,
                                                                       'from': transfer.from_address, 'to': None}

        else:
            self.totals[transfer.to_address] = {
                transfer.value_id: {"sent": 0, "received": transfer.value, 'to': None, 'from': transfer.from_address}}
