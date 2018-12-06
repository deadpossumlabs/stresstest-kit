import json
import os
import time
import traceback

from hexbytes import HexBytes
from extractors.EtherTransferExtractor import EtherTransferExtractor
from extractors.TokenTransferExtractor import TokenTransferExtractor
from helper import FOLDERS, HexJsonEncoder
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction
from solc import compile_source


class Tests:
    DIR_CONTRACTS = "./contracts/"

    def __init__(self, w3, logger, inspector):
        self.w3 = w3
        self.logger = logger
        self.inspector = inspector
        self.funcs = {
            "test_many": (self.test_many_light_trans, True),
            "test_heavy": (self.test_many_heavy_trans, True),
            "test_expensive": (self.test_expensive_trans, True),
            "test_same": (self.send_same_trans, False),
            "balance": (self.get_balance, False),
            "deploy": (self.deploy_contract, False),
            "accounts": (self.get_accounts_info, False),
            "get_trans": (self.get_transaction_info, False),
            "send_trans": (self.send_transaction_from_contract, False),
            "send_eth": (self.send_eth, False),
            "unlock": (self.unlock_account, False),
            "unlocks": (self.unlock_accounts, False),
            "new_acc": (self.set_account, False),
            "private": (self.get_private_key, False),
            "privates": (self.get_private_keys, False),
            # "node": (self.node_info, False),
        }

    def is_thread(self, func_name):
        if func_name in self.funcs:
            return self.funcs[func_name][1]
        return None

    def start_test(self, func_name, args):

        if func_name in self.funcs:
            try:
                self.funcs[func_name][0](*args)
            except TypeError as e:
                self.logger.error("\tError in command {0}{1}: {2}".format(func_name, args, e))
                return
            except Exception as e:
                self.logger.error("\tError in command {0}{1}: {2}".format(func_name, args, e))
        else:
            self.logger.error("\tUnresolved command: \"{0}\"".format(func_name))


                                                ## Tests with node ##
    def node_info(self):
        # self.w3.admin.nodeInfo()
        self.logger.info("\t{0}".format(self.w3.net))

    def send_eth(self, account1, account2, funds):
        sender = self.w3.toChecksumAddress(account1[0])
        sender_key = account1[1]
        receiver = self.w3.toChecksumAddress(account2[0])
        trans_param = dict(
            nonce=self.w3.eth.getTransactionCount(sender),
            gasPrice=self.w3.eth.gasPrice,
            gas=21000,
            to=receiver,
            value=hex(funds)
        )
        signed_txn = self.w3.eth.account.signTransaction(trans_param, sender_key)

        trans = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        trans_hash = HexBytes(trans)
        self.logger.info("\tSend transaction: {0}".format(trans_hash.hex()))

    def test_many_light_trans(self, accounts, time_live):

        """
        Checking the network for resistance to a large number of light
        transaction requests
        :param time_live: means how long will the thread run
        :param accounts: a list or a tuple that includes address and a key
                        from two accounts for transferring Ethereum
        """

        start_time = time.time()
        address1 = self.w3.toChecksumAddress(accounts[0])
        key1 = accounts[1]
        address2 = self.w3.toChecksumAddress(accounts[2])
        nonce = self.w3.eth.getTransactionCount(address1)
        while True:
            try:
                trans_param = dict(
                    nonce=nonce,
                    gasPrice=self.w3.eth.gasPrice,
                    gas=21000,
                    to=address2,
                    value=hex(10000000000000000)
                )
                signed_txn = self.w3.eth.account.signTransaction(trans_param, key1)

                trans = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

                trans_hash = HexBytes(trans)
                self.logger.info("\tSend transaction: {0} with nonce: {1}".format(trans_hash.hex(), nonce))
            except ValueError as e:
                self.logger.warning("\t{0}".format(e.args[0]["message"]))
                continue

            except Exception as e:
                raise e
            finally:
                nonce += 1
                if time.time() - start_time >= time_live:
                    break

    def test_many_heavy_trans(self, accounts, time_live, cnt_address, func_name, abi_file, args=None):
        gas = self.w3.eth.gasPrice
        start_time = time.time()
        acct = self.w3.eth.account.privateKeyToAccount(accounts[1])
        nonce = self.w3.eth.getTransactionCount(acct.address)

        while True:
            try:
                self.send_transaction_from_contract(accounts[1], cnt_address, func_name, abi_file, nonce,
                                                    args=args, gasprice=gas)
            except ValueError as e:
                self.logger.info("\tWarning: {0}".format(e.args[0]["message"]))
                continue
            finally:
                if time.time() - start_time >= time_live:
                    break
                nonce += 1

    def test_expensive_trans(self, accounts, time_live, cnt_address, func_name, abi_file, args=None):
        gas = 100000000000000000000
        start_time = time.time()
        acct = self.w3.eth.account.privateKeyToAccount(accounts[1])
        nonce = self.w3.eth.getTransactionCount(acct.address)

        while True:
            try:
                self.send_transaction_from_contract(accounts[1], cnt_address, func_name, abi_file, nonce,
                                                    args=args, gasprice=gas)
            except ValueError as e:
                self.logger.info("\tWarning: {0}".format(e.args[0]["message"]))
                continue
            finally:
                if time.time() - start_time >= time_live:
                    break
                nonce += 1


    def send_same_trans(self, sender_addr, sender_priv, receive_addr):

        """
        Check network for sending identical transactions
        :param receive_addr: receive eth-address
        :param sender_priv: sender eth-private key
        :param sender_addr: sender eth-address
        :return: None
        """
        sender_addr = self.w3.toChecksumAddress(sender_addr)
        receive_addr = self.w3.toChecksumAddress(receive_addr)
        while True:
            try:
                params = dict(
                    nonce=self.w3.eth.getTransactionCount(sender_addr),
                    gasPrice=self.w3.eth.gasPrice,
                    gas=100000,
                    to=receive_addr,
                    value=hex(10000000000000000)
                )
                params2 = params.copy()
                params2["value"] = hex(1)
                params2["gasPrice"] += 10000000000000000000
                signed_txn = self.w3.eth.account.signTransaction(params, sender_priv)
                _signed_txn = self.w3.eth.account.signTransaction(params2, sender_priv)
                trans1 = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                trans2 = self.w3.eth.sendRawTransaction(_signed_txn.rawTransaction)
                trans1_hash = HexBytes(trans1)
                trans2_hash = HexBytes(trans2)
                self.logger.info("\tSend same transactions:\n"
                                 "\t\t\t\t\t\t\t\t\t\t\t{0}\n"
                                 "\t\t\t\t\t\t\t\t\t\t\t{1}".format(trans1_hash.hex(), trans2_hash.hex()))
                return None
            except ValueError as e:
                self.logger.warning("\t{0}".format(e.args[0]["message"]))
                time.sleep(2)
                continue

            except Exception as e:
                raise e


                                            ## Tests with accounts ##

    def unlock_account(self, address, passphrase):
        address = self.w3.toChecksumAddress(address)
        try:
            is_unlock = self.w3.personal.unlockAccount(address, passphrase)
        except ValueError as e:
            if e.args[0]["data"] == "InvalidAccount":
                self.logger.error("\tCannot find account: {0}".format(address))
            else:
                self.logger.error("\tUnhandled error: {0}".format(e))
            return
        message = "Account {} is not unlocked. Use right passphrase.".format(address)
        if is_unlock:
            message = "Account {} is successfully unlocked.".format(address)
        self.logger.info("\t" + message)

    def unlock_accounts(self, addresses, passphrase):
        for address in addresses:
            address = self.w3.toChecksumAddress(address)
            try:
                is_unlock = self.w3.personal.unlockAccount(address, passphrase)
            except ValueError as e:
                if e.args[0]["data"] == "InvalidAccount":
                    self.logger.error("\tCan't find account: {0}.".format(address))
                elif e.args[0]["data"] == "InvalidPassword":
                    self.logger.error("\tInvalid password: {0}.".format(address))
                else:
                    self.logger.error("Unhandled error: {0}.".format(e))
                continue
            message = "Account {} is not unlocked. Use right passphrase.".format(address)
            if is_unlock:
                message = "Account {} is successfully unlocked.".format(address)
            self.logger.info("\t" + message)

    def get_balance(self, address):

        """
        Get balance from account address
        :param address: account address
        :return: None
        """

        address = self.w3.toChecksumAddress(address)
        balance = self.w3.eth.getBalance(address)
        self.logger.info("\tBalance of account {0}:{1}".format(address, balance))
        return balance

    def get_accounts_info(self):
        accounts = self.w3.personal.listAccounts
        for i in range(len(accounts)):
            accounts[i] = accounts[i].lower()
        logs = "\tAccounts:"
        for account in accounts:
            account = "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + account
            logs += account
        logs += "\n\t"
        self.logger.info(logs)

    def get_accounts(self):
        accounts = self.w3.eth.accounts
        for i in range(len(accounts)):
            accounts[i] = accounts[i].lower()
        return accounts

    def set_account(self, passphrase, priv_key, count=1):
        for i in range(count):
            address = self.w3.personal.importRawKey(priv_key, passphrase)
            self.logger.info("\tNew account: {0}".format(address))

    def get_private_key(self, file, password):
        with open(FOLDERS["accounts"] + file) as keyfile:
            abi = json.loads(keyfile.read())
            address = "0x" + abi["address"]
            try:
                private_key_bin = self.w3.eth.account.decrypt(abi, password)
            except ValueError as e:
                self.logger.error("\tCannot get private key. "
                                  "Make sure that you enter the correct password. ({0})".format(e))
                return
            _private_key = private_key_bin.hex()  # have 0x
            private_key = _private_key.replace("0x", "")
            self.logger.info("\tPrivate key of {0}: {1}".format(address, private_key))

    def get_private_keys(self, password):
        gen = os.walk("./accounts/")
        accounts = next(gen)[2]
        for account in accounts:
            with open(FOLDERS["accounts"] + account) as keyfile:
                abi = json.loads(keyfile.read())
                address = "0x" + abi["address"]
                try:
                    private_key_bin = self.w3.eth.account.decrypt(abi, password)
                except ValueError as e:
                    self.logger.error(
                        "\tCannot get private key for address {0}: {1}. "
                        "Make sure that you enter the correct password. ({2})".format(address, account, e))
                    continue
                _private_key = private_key_bin.hex()  # 0x...
                private_key = _private_key.replace("0x", "")
                self.logger.info("\tPrivate key of {0}: {1}".format(address, private_key))

                                        ## Tests with contracts and transactions ##

    def deploy_contract(self, file_sol, priv_key):
        with open(self.DIR_CONTRACTS + file_sol, "r") as f:
            source = f.read()

        compiled_sol = compile_source(source)

        contract_id, contract_interface = compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        contract = self.w3.eth.contract(
            abi=abi,
            bytecode=bytecode
        )
        acct = self.w3.eth.account.privateKeyToAccount(priv_key)
        self.logger.info("\tDeploying...")
        tx_hash = contract.constructor().buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 1728712,
            'gasPrice': self.w3.eth.gasPrice
        })
        signed = acct.signTransaction(tx_hash)
        trans = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        address = self.get_transaction_info(trans.hex())["contractAddress"]

        with open(FOLDERS["abi"] + file_sol.replace("sol", "abi"), "w") as f:
            abi_json = json.dumps(abi, indent=4)
            f.write(abi_json)

        self.logger.info("\tSuccessfully deployed {0} to: {1} and saved ABI".format(file_sol, address))

    def contract_functions(self, address):
        pass

    def contract_function(self, contract):
        pass

    def get_transaction_info(self, hash_trans):
        time.sleep(3)
        trans_info = self.w3.eth.getTransactionReceipt(hash_trans)
        if not trans_info:
            self.logger.error("\t Transaction {0} is not found.".format(hash_trans))
            return
        trans_info_pretty = json.dumps(dict(trans_info), cls=HexJsonEncoder, indent=48)
        self.logger.info("\tTransaction {0}:\n"
                         "\t\t\t\t\t\t\t\t\t\t\t{1}".format(hash_trans, trans_info_pretty))
        return trans_info

    def send_transaction_from_contract(self, priv_key, cnt_address, func_name, abi_file, nonce,
                                       to=None, value=None, args=None, gasprice=None):

        cnt_address = self.w3.toChecksumAddress(cnt_address)
        acct = self.w3.eth.account.privateKeyToAccount(priv_key)

        with open(FOLDERS["abi"] + abi_file, 'r') as file:
            abi = json.loads(file.read())

        contract = self.w3.eth.contract(
            address=cnt_address,
            abi=abi
        )
        if not gasprice:
            gasprice = self.w3.eth.gasPrice
        trans_param = {
            "from": acct.address,
            "nonce": nonce,
            "gasPrice": gasprice,
        }
        if to:
            trans_param["to"] = to
        if value:
            trans_param["value"] = value
        if args:
            func_args = []
            if type(args) != list or type(args) != tuple:
                func_args.append(args)
            else:
                func_args = args
            txn_hash = contract.functions[func_name](*func_args).buildTransaction(trans_param)
        else:
            txn_hash = contract.functions[func_name]().buildTransaction(trans_param)
        signed = acct.signTransaction(txn_hash)
        trans = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        trans_address = HexBytes(trans).hex()
        self.logger.info("\tSend transaction '{2}' from contract: {3}. Hash: {0} with nonce: {1}".format(trans_address, nonce,
                                                                                                   func_name,
                                                                                                   cnt_address))

                                                            ## Other tests ##

    def import_block(self, block):
        txs = []
        for tx_dict in block['transactions']:
            try:
                tx = TransactionMapper.json_dict_to_transaction(tx_dict)
                self.logger.info("Importing ", extra=tx_dict)
                for transfer in self.get_tx_value_transfers(tx):
                    tx.add_transfer(transfer)
                    txs.append(tx)

            except BaseException as e:
                self.logger.error(e, exc_info=True, extra=tx_dict)

        return txs

    def get_tx_value_transfers(self, transaction: Transaction):
        transfers = []
        try:
            if transaction.block_number is None:
                return []

            for transfer in TokenTransferExtractor.extract(transaction):
                transfers.append(transfer)

            for transfer in EtherTransferExtractor.extract(transaction):
                transfers.append(transfer)

        except BaseException as e:
            self.logger.error(e, {"trace": traceback.format_exc(), "txid": transaction.hash})

        return transfers
