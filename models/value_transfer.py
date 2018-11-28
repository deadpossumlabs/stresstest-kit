TYPE_ETHER = 1
TYPE_TOKEN = 2


class ValueTransfer(object):
    from_address = None
    to_address = None
    value = None
    type = 0
    value_id = ""
    transaction_hash = None

    def __init__(self):
        pass


class TokenTransfer(ValueTransfer):
    def __init__(self):
        self.type = TYPE_TOKEN


class EtherTransfer(ValueTransfer):

    def __init__(self):
        self.value_id = "0"
        self.type = TYPE_ETHER
