from eth_rpc_api import ParityEthJsonRpc


def infura_config(binder):
    binder.bind_to_constructor(ParityEthJsonRpc,
                               lambda: ParityEthJsonRpc("mainnet.infura.io/4201067680114343b90b8273eb1243af",
                                                        tls=True))


def base_config(binder):
    binder.bind_to_constructor(ParityEthJsonRpc, lambda: ParityEthJsonRpc("status.moonshrd.io"))


def localhost_config(binder):
    binder.bind_to_constructor(ParityEthJsonRpc, lambda: ParityEthJsonRpc("localhost:8545"))
