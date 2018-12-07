import os
from types import FunctionType

from conf import infura_config, base_config
from controller import TestController
from helper import FOLDERS

if __name__ == '__main__':

    for folder in FOLDERS:
        if not os.path.exists(FOLDERS[folder]):
            os.mkdir(FOLDERS[folder])

    def methods(cls):
        return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]

    m = methods(TestController)

    # default: HTTP://127.0.0.1:7545
    # WEB3_PROVIDER_URI = "HTTP://127.0.0.1:8545"
    WEB3_PROVIDER_URI = "HTTP://104.248.67.155:8545"
    # WEB3_PROVIDER_URI = "HTTP://192.168.1.19:8545"
    # test1 = TestController(WEB3_PROVIDER_URI, infura_config)
    # test2 = TestController(WEB3_PROVIDER_URI, base_config)

    # lock1 = RLock()
    # lock2 = RLock()
    # @todo если количество аккаунтов большое, то при тесте с дорогими функциями контракта падают потоки - timeout
    # accounts = (["0x6f01Df94aD13495c9CDe2dc2aE272e5e559834B4",
    #              "f168194b09d855dcfee49d73f237ac3f26f3a5fbaff19f24af6283418f336eab"],
    #             ["0xfBfFaa86d30053418Eb5596334FAfE35415E8706",
    #              "2d7faf62bdc964e8723f148b129c66723478fbbf05d8de41f39edc24bae581ed"],
    #             ["0x8bbbc4CD72Dd576ED731080d5cc36E411d9c326d",
    #              "a9dc7f48730076af0e923bf4eb43ff459d78ad467247b3e66637b3e4cc913ab0"],
    #             ["0xFF66A2921b81FdeD548734b716cEA382ca0ec0E6",
    #              "265d027ce739bd0e38d6c6842dcc54c5f0b576b9c85dd269ba1f4b533badc1f9"],
    #             ["0x5867Afc85076C6243a74E4Fe2Ff4ea95719E293e",
    #              "be8aa0b785ab06756247f04e446fff526f8ede1864d172bc8db1eeaccc8f6c32"],
    #             ["0xaf073f0849e779202d0A92a12128C3b144856D6f",
    #              "c8959bd1b6835f5a367697e7456655aa026009cbf17bbfe9c87c13ea3c1b8ac3"],
    #             ["0x9c35Df66Fe1Df12831C1ECAd1983DA0aAefd6658",
    #              "86f7c68a91e7e6dbc6ad149faccf46783acadb64f5f0e1022b08b6923c43186f"],
    #             ["0x5A2569dC467c30c76D7C1E54536fd15675654A1F",
    #              "8735cc620363abffe94f67c791c4a095d148e29e21e71f21fd3a902c177b8c4c"],
    #             ["0xb28FF41AB43d14dfCBcD0D9135b420e667d69d1A",
    #              "e6b79ce756caae056bbc21519a7ad54f73d037250ddec5c5f884be89ff68cfde"],
    #             ["0x425a394c5F54Ab037CdFd23e6A622Fe4c6cf8DC6",
    #              "2fe52627b246f5e3480a6c3a1cd5ce26341978a0b73f08a66c7a803cc29feedb"],
    #             )
    #
    accounts = (
        ["0x40fdee788a2b2cce016660fc5e7a3efeaaf0a860",
         "4B840E1D567A493B9B21308D2C85616C56CD664C97520B041F539EC5F35F62AA"],
        ["0x1c3b9974c14381c932506742a79295a779307101",
         "68c83226fab45601676192434e7755073ce9a21f60485fc5edcd534614a15dfb"],     # 1 2 3
        ["0x49d80828f56779f7ffc83114dfd7ce0aa9ce811c",
         "390527faae26b21a32e8f220919ae9af626f6f09a20013ae1b960297ea36ddcc"],     # 123
        ["0x1f642cdc8ee32f586478bc7d5f14303f0fc0115d",
         "388fd455f5d3d785a7dce044f6cb60055a3cb4c282401d0b8dfc69c8ec7233aa"],     # 456
        ["0x8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2",
         "6d2f23ea27162fbb170f97b4840a272239be8b8d20c86b76f8e9d9193083546b"],     # 789
        ["0x548daa8f9df9cf0161607736b316e0f9f008cd33",
         "6fec9d5ae596f97e102d7d47f13330101f7e72b03a324f63e29e531dbba1d983"],
        ["0x91548ab5661e0a0f83c12ee1ad59a5bd55146643",
         "a17f8fef97056b3584e0c497459176411ba89b04c460cb1a788563c6ac8d70cc"],
        ["0xe2d0e97f115a773c67268fd719daeb9ddedf605f",
         "aca8d031af11a91972480ea473fc106ca075d8511df6d3ff6abe42c0407877b5"],
        ["0xe39e686e976f3360879bcf195761ccf45412a3d7",
         "0eabacfa58903c3d6928c3c92ede9b8c4167793c0ce330d1bf1bba8f1314d431"],
    )

    addresses = [account[0] for account in accounts]
    priv_keys = [account[1] for account in accounts]

    tests = TestController(WEB3_PROVIDER_URI, infura_config, accounts)

                                                    # Tests

    # tests.add_test("accounts")
    # tests.add_test("node")

    # tests.add_test("unlocks", (addresses, "1 2 3"))
    # tests.add_test("privates", ("123", ))
    # tests.add_test("private", ("UTC--2018-12-03T15-08-09.573673621Z--1f642cdc8ee32f586478bc7d5f14303f0fc0115d", "456"))
    # tests.add_test("private", ("UTC--2018-12-03T15-08-28.053421410Z--8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2", "789"))
    # tests.add_test("new_acc", ("0eabacfa58903c3d6928c3c92ede9b8c4167793c0ce330d1bf1bba8f1314d431", "123"))

    # tests.add_test("new_acc", ("123", "390527faae26b21a32e8f220919ae9af626f6f09a20013ae1b960297ea36ddcc"))
    # tests.add_test("deploy", ("test.sol", accounts[0][1]))

    # tests.add_test("unlocks", (addresses, "123"))
    # tests.add_test("unlock", ("0x49d80828f56779f7ffc83114dfd7ce0aa9ce811c", "1 2 3"))
    # tests.add_test("unlock", ("0x1f642cdc8ee32f586478bc7d5f14303f0fc0115d", "456"))
    # tests.add_test("unlock", ("0x8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2", "789"))

    # tests.add_test("get_trans", ("0xff28bd3c788b7d9cc90f47a4670e3b1a6dd720579797f4c63e631c2b34b6b744", ))

    # for account in accounts:
    #     tests.add_test("balance", (account[0], ))

    # tests.add_test("send_eth", (accounts[0], accounts[1], 100000000000000000))  # = 0.1 Eth
    # tests.add_test("send_eth", (accounts[2], accounts[5], 10000000000000000000000000))  # = 10000 Eth
    # tests.add_test("send_eth", (accounts[3], accounts[6], 10000000000000000000000000))  # = 10000 Eth
    # tests.add_test("send_eth", (accounts[4], accounts[7], 10000000000000000000000000))  # = 10000 Eth
    # tests.add_test("send_eth", (accounts[2], accounts[8], 100000000000000000000000000))  # = 100000 Eth
    # tests.add_test("nonce", (addresses[0], ))
    tests.add_test("send_trans", (priv_keys[1], "0xa981c1D103F000387fbd025ccc403EA58353EF48", "empty", "test.abi", 1093))

    # tests.add_test("test_same", (accounts[0][0], accounts[0][1], accounts[1][0]))
    # tests.add_test("test_many", (2,), flows=10)
    # tests.add_test("test_expensive", (5, "0xa981c1D103F000387fbd025ccc403EA58353EF48", "empty", "test.abi"), flows=10)
    # tests.add_test("test_heavy", (20, "0xa981c1D103F000387fbd025ccc403EA58353EF48", "empty", "test.abi"), flows=10)
    # tests.add_test("test_heavy", (1, "0x038c7623c7a9d730170297De7B4d33Bb99dF98eD", "empty", "test.abi"), flows=10) # ganache

    tests.start_tests()
