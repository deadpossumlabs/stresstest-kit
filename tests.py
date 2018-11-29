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
            "sametrans": self.send_same_trans,
            "balance": self.get_balance,
            "deploy": self.deploy_contract,
            "accounts": self.get_accounts,
            "get_trans": self.get_transaction_info,
            "send": self.send_transaction_from_contract
            # "new_acc": self.set_account,
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

    def test_many_light_trans(self, time_live, account):

        """
        Checking the network for resistance to a large number of light
        transaction requests
        :param time_live: means how long will the thread run
        :param account: a list or a tuple that includes two addresses and a keys
                        from accounts for transferring Ethereum to each other
        """
        accounts = self.get_accounts()
        index_account = accounts.index(account[0])
        index_next_account = index_account + 1
        if index_next_account == len(accounts):
            index_next_account = 0
        next_account = accounts[index_next_account]
        start_time = time.time()
        address1 = self.w3.toChecksumAddress(account[0])
        key1 = account[1]
        address2 = self.w3.toChecksumAddress(next_account)
        while True:
            try:
                trans_param = dict(
                        nonce=self.w3.eth.getTransactionCount(address1),
                        gasPrice=self.w3.eth.gasPrice,
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
            finally:
                if time.time() - start_time >= time_live:
                    break

    def test_many_heavy_trans(self, time_live, cnt_address, func_name, abi_file, account):
        print(account)
        start_time = time.time()
        while True:
            self.send_transaction_from_contract(account[1], cnt_address, func_name, abi_file)
            if time.time() - start_time >= time_live:
                break

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
                params2["gasPrice"] += 10000000000
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

    def get_balance(self, address):

        """
        Get balance from account address
        :param address: account address
        :return: None
        """

        address = self.w3.toChecksumAddress(address)
        balance = self.w3.eth.getBalance(address)
        self.logger.info("\tBalance of account {0}:{1}".format(address, balance))

    def get_accounts(self):
        accounts = self.w3.eth.accounts
        logs = "\tAccounts:"
        for account in accounts:
            account = "\n\t\t\t\t\t\t\t\t\t\t\t" + account
            logs += account
        logs += "\n\t"
        self.logger.info(logs)
        return accounts

    def set_account(self):
        self.logger.info(self.w3.eth.accounts)


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
        tx_hash = contract.constructor().buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 1728712,
            'gasPrice': self.w3.toWei('21', 'gwei')
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

    def send_transaction_from_contract(self, priv_key, cnt_address, func_name, abi_file, to=None, value=None):

        cnt_address = self.w3.toChecksumAddress(cnt_address)
        acct = self.w3.eth.account.privateKeyToAccount(priv_key)

        with open(FOLDERS["abi"] + abi_file, 'r') as file:
            abi = json.loads(file.read())

        contract = self.w3.eth.contract(
            address=cnt_address,
            abi=abi
        )
        trans_param = {
            "from": acct.address,
            "nonce": self.w3.eth.getTransactionCount(acct.address)
        }
        if to and value:
            trans_param["to"] = to
            trans_param["value"] = value
        txn_hash = contract.functions[func_name]().buildTransaction(trans_param)
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
