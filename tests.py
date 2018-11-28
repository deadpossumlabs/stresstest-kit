import time
import traceback

from hexbytes import HexBytes
from web3 import Web3, HTTPProvider

from extractors.EtherTransferExtractor import EtherTransferExtractor
from extractors.TokenTransferExtractor import TokenTransferExtractor
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction
from solc import compile_source, compile_files, compile_standard
from web3.providers.eth_tester import EthereumTesterProvider


class Tests:

    def __init__(self, w3, logger, inspector):
        self.w3 = w3
        self.logger = logger
        self.inspector = inspector
        self.funcs = {
            "chckserver": self.check_server_load,
            "sametrans": self.send_same_trans,
            "balance": self.get_balance,
            "deploy": self.deploy_contract,
            "accounts": self.get_accounts,
            "node": self.node_info,
            "new_acc": self.set_account,
            "get_trans": self.get_transaction_info,
        }

    def start_test(self, func_name, args):
        if func_name in self.funcs:
            try:
                self.funcs[func_name](*args)
            except TypeError as e:
                self.logger.error("\tError in command {0}{1}: {2}".format(func_name, args, e))
                return
            except Exception as e:
                self.logger.error("Error in command {0}(): {1}".format(func_name, e))
        else:
            self.logger.error("\tUnresolved command: \"{0}\"".format(func_name))

                                                ## Tests with node ##
    def node_info(self):
        self.w3.admin.nodeInfo()
        self.logger.info("\t{0}".format(self.w3.admin.nodeInfo))

    def check_server_load(self, time_live, accounts):

        """
        Checking the network for resistance to a large number of
        transaction requests
        :param time_live: means how long will the thread run
        :param accounts: a list or a tuple that includes two addresses and a keys
                        from accounts for transferring Ethereum to each other
        # :param lock: used to restrict block access threads+
        """
        start_time = time.time()
        address1 = self.w3.toChecksumAddress(accounts[0])
        key1 = accounts[1]
        address2 = self.w3.toChecksumAddress(accounts[2])
        key2 = accounts[3]
        while True:
            try:
                # lock.acquire()
                accounts = dict(
                        nonce=self.w3.eth.getTransactionCount(address1),
                        gasPrice=self.w3.eth.gasPrice,
                        gas=100000,
                        to=address2,
                        value=hex(10000000000000000)
                )
                signed_txn = self.w3.eth.account.signTransaction(accounts, key1)

                trans = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                # lock.release()

                trans_hash = HexBytes(trans)
                self.logger.info("\tSend transaction: {0}".format(trans_hash.hex()))
                # address1, address2 = address2, address1
                # key1, key2 = key2, key1
                # lock.acquire()
                # block = self.inspector.get_next_block()
                # # lock.release()
                # for tx in block['transactions']:
                #     # lock.acquire()
                #     params = dict(
                #         nonce=self.w3.eth.getTransactionCount(address1),
                #         gasPrice=self.w3.eth.gasPrice,
                #         gas=100000,
                #         data=tx['input'],
                #         to=address2,
                #         value=hex(10000000000000000)
                #     )
                #     # lock.release()
                #     signed_txn = self.w3.eth.account.signTransaction(params, key1)
                #     trans = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                #     address1, address2 = address2, address1
                #     key1, key2 = key2, key1
                #     trans_hash = HexBytes(trans)
                #     self.logger.info("\tSend transaction: {0}".format(trans_hash.hex()))
                #     address1, address2 = address2, address1
                #     key1, key2 = key2, key1
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

    def send_same_trans(self, lock, params):

        """
        Check network for sending identical transactions
        :param params: a list or a tuple that includes two addresses and a keys from accounts
        for transferring Ethereum to each other
        :param lock: used to restrict block access threads
        :return: None
        """
        address1 = self.w3.toChecksumAddress(params[0])
        key1 = params[1]
        address2 = self.w3.toChecksumAddress(params[2])
        key2 = params[3]

        while True:
            try:
                lock.acquire()
                block = self.inspector.get_next_block()
                lock.release()
                for tx in block['transactions']:
                    params = dict(
                        nonce=self.w3.eth.getTransactionCount(address1),
                        gasPrice=self.w3.eth.gasPrice,
                        gas=100000,
                        data=tx['input'],
                        to=address2,
                        value=hex(10000000000000000)
                    )
                    params2 = params.copy()
                    params2["value"] = hex(10000000000000001)
                    signed_txn = self.w3.eth.account.signTransaction(params, key1)
                    _signed_txn = self.w3.eth.account.signTransaction(params2, key1)
                    trans1 = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    trans2 = self.w3.eth.sendRawTransaction(_signed_txn.rawTransaction)
                    trans1_hash = HexBytes(trans1)
                    trans2_hash = HexBytes(trans2)
                    # print(chis1, chis2)
                    self.logger.info("\tSend same transactions:\n"
                                     "\t\t\t\t\t\t\t\t\t\t\t{0}\n"
                                     "\t\t\t\t\t\t\t\t\t\t\t{1}".format(trans1_hash.hex(), trans2_hash.hex()))
                    # print(tx)
                    return None
            except ValueError as e:
                self.logger.warning("\t{0}".format(e.args[0]["message"]))
                if "Insufficient funds. The account you tried to send transaction from does not have enough funds" not in e.args[0]["message"]:
                    continue
                address1, address2 = address2, address1
                key1, key2 = key2, key1

                                            ## Tests with accounts ##

    def get_balance(self, address):

        """
        Get balance from account address
        :param address: account address
        :return: None
        """
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

    def set_account(self):
        self.logger.info(self.w3.eth.accounts)



                                            ## Tests with contracts and transactions ##
    def contract_functions(self):
        # contract.all_functions()
        pass

    def contract_function(self, contract):
        # contract.get_function_by_signature('identity(uint256,bool)')
        pass

    def deploy_contract(self, file_sol, account):
        with open(file_sol, "r") as f:
            source = f.read()
        compiled_sol = compile_source(source)

        contract_id, contract_interface = compiled_sol.popitem()
        contract = self.w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin'])
        acct = self.w3.eth.account.privateKeyToAccount(account[1])
        tx_hash = contract.constructor().buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 1728712,
            'gasPrice': self.w3.toWei('21', 'gwei')
        })
        signed = acct.signTransaction(tx_hash)
        trans = HexBytes(self.w3.eth.sendRawTransaction(signed.rawTransaction))
        address = self.get_transaction_info(trans)["contractAddress"]
        # trans_hash = HexBytes(trans)
        self.logger.info("\tSuccessfully deployed {0} to: {1}".format(file_sol, address))

    def get_transaction_info(self, hash):
        trans_info = self.w3.eth.getTransactionReceipt(hash)
        self.logger.info("\tTransaction {0}:{1}".format(hash.hex(), trans_info))
        return trans_info

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
