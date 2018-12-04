import json
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
            "test_many": self.test_many_light_trans,
            "test_heavy": self.test_many_heavy_trans,
            "test_expensive": self.test_expensive_trans,
            "sametrans": self.send_same_trans,
            "balance": self.get_balance,
            "deploy": self.deploy_contract,
            "accounts": self.get_accounts_info,
            "get_trans": self.get_transaction_info,
            "send_trans": self.send_transaction_from_contract,
            "send_eth": self.send_eth,
            "unlock": self.unlock_account,
            "new_acc": self.set_account,
            "private": self.get_private_key,
            # "node": self.node_info,
        }

    def start_test(self, func_name, args):
        if func_name in self.funcs:
            # try:
            self.funcs[func_name](*args)
            # except TypeError as e:
            #     self.logger.error("\tError in command {0}{1}: {2}".format(func_name, args, e))
            #     return
            # except Exception as e:
            #     self.logger.error("\tError in command {0}{1}: {2}".format(func_name, args, e))
        else:
            self.logger.error("\tUnresolved command: \"{0}\"".format(func_name))


                                                ## Tests with node ##
    def node_info(self):
        self.w3.admin.nodeInfo()
        self.logger.info("\t{0}".format(self.w3.admin.nodeInfo))

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

    def test_many_light_trans(self, time_live, accounts):

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
                self.logger.info("\tSend transaction: {0}".format(trans_hash.hex()))
            except ValueError as e:
                self.logger.warning("\t{0}".format(e.args[0]["message"]))
                # time.sleep(2)
                # address1, address2 = address2, address1
                # key1, key2 = key2, key1
                continue

            except Exception as e:
                # try:
                #     lock.release()
                # except Exception:
                #     pass
                # self.logger.error("\tUnhandled error:{0}{1}".format(e.__class__.__name__, e))
                raise e
            finally:
                nonce += 1
                if time.time() - start_time >= time_live:
                    break

    def test_many_heavy_trans(self, time_live, cnt_address, func_name, abi_file, accounts):
        value1 = 0
        value2 = 100000
        gas1 = self.w3.eth.gasPrice
        gas2 = gas1 + 1000
        start_time = time.time()
        acct1 = self.w3.eth.account.privateKeyToAccount(accounts[1])
        acct2 = self.w3.eth.account.privateKeyToAccount(accounts[3])

        nonce1 = self.w3.eth.getTransactionCount(acct1.address)
        nonce2 = self.w3.eth.getTransactionCount(acct2.address)

        while True:
            self.send_transaction_from_contract(accounts[1], cnt_address, func_name, abi_file, nonce1,
                                                args=[value1], gasprice=gas1)
            # time.sleep(1)
            # self.send_transaction_from_contract(accounts[3], cnt_address, func_name, abi_file, nonce2,
            #                                     args=[value2], gasprice=gas2)
            if time.time() - start_time >= time_live:
                break
            nonce1 += 1
            nonce2 += 1
            value1 += 1
            value2 += 1
            gas1 += 10000000000000
            gas2 += 11000000000000
            # time.sleep(1)

    def test_expensive_trans(self, time_live, accounts):

        start_time = time.time()
        address1 = self.w3.toChecksumAddress(accounts[0])

        key1 = accounts[1]
        address2 = self.w3.toChecksumAddress(accounts[2])
        nonce = self.w3.eth.getTransactionCount(address1)
        while True:
            try:
                trans_param = dict(
                    nonce=nonce,
                    gasPrice=100000000000000000,
                    gas=100000,
                    to=address2,
                    value=hex(10000000000000000)
                )
                signed_txn = self.w3.eth.account.signTransaction(trans_param, key1)

                trans = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

                trans_hash = HexBytes(trans)
                self.logger.info("\tSend transaction: {0}".format(trans_hash.hex()))
            except ValueError as e:
                self.logger.warning("\t{0}".format(e.args[0]["message"]))
                # time.sleep(2)
                # address1, address2 = address2, address1
                # key1, key2 = key2, key1
                continue

            except Exception as e:
                # try:
                #     lock.release()
                # except Exception:
                #     pass
                # self.logger.error("\tUnhandled error:{0}{1}".format(e.__class__.__name__, e))
                raise e
            finally:
                nonce += 1
                if time.time() - start_time >= time_live:
                    break
        pass

    def send_same_trans(self, accounts):

        """
        Check network for sending identical transactions
        :param accounts: a list or a tuple that includes two addresses and a keys from accounts
        for transferring Ethereum to each other
        :return: None
        """
        address1 = self.w3.toChecksumAddress(accounts[0][0])
        key1 = accounts[0][1]
        address2 = self.w3.toChecksumAddress(accounts[1][0])

        while True:
            try:
                params = dict(
                    nonce=self.w3.eth.getTransactionCount(address1),
                    gasPrice=self.w3.eth.gasPrice,
                    gas=100000,
                    # data=tx['input'],
                    to=address2,
                    value=hex(10000000000000000)
                )
                params2 = params.copy()
                params2["value"] = hex(10000000000000001)
                params2["gasPrice"] += 10000000000000
                signed_txn = self.w3.eth.account.signTransaction(params, key1)
                _signed_txn = self.w3.eth.account.signTransaction(params2, key1)
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
                # address1, address2 = address2, address1
                # key1, key2 = key2, key1
                continue

            except Exception as e:
                # try:
                #     lock.release()
                # except Exception:
                #     pass
                # self.logger.error("\tUnhandled error:{0}{1}".format(e.__class__.__name__, e))
                raise e


                                            ## Tests with accounts ##

    def unlock_account(self, address, passphrase):
        address = self.w3.toChecksumAddress(address)
        try:
            is_unlock = self.w3.personal.unlockAccount(address, passphrase)
        except ValueError as e:
            if e.args[0]["data"] == "InvalidAccount":
                self.logger.error("\tCannot find account.")
            else:
                self.logger.error("Unhandled error: {0}".format(e))
            return
        message = "Account {} is not unlocked. Use right passphrase".format(address)
        if is_unlock:
            message = "Account {} is succesfully unlocked".format(address)
        self.logger.info(message)

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
            account = "\n\t\t\t\t\t\t\t\t\t\t\t" + account
            logs += account
        logs += "\n\t"
        self.logger.info(logs)
        return accounts

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
                self.logger.error("\tCannot get private key. Make sure that you enter the correct password. ({0})".format(e))
                return
            _private_key = private_key_bin.hex() # 0x...
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
        trans_info = self.w3.eth.getTransactionReceipt(hash_trans)
        if not trans_info:
            time.sleep(3)
            trans_info = self.w3.eth.getTransactionReceipt(hash_trans)
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
        func_args = []
        if args:
            for arg in args:
                func_args.append(arg)
        txn_hash = contract.functions[func_name](*func_args).buildTransaction(trans_param)
        signed = acct.signTransaction(txn_hash)
        trans = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        trans_address = HexBytes(trans).hex()
        self.logger.info("\tSuccessfully send transaction: {0}".format(trans_address))


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
