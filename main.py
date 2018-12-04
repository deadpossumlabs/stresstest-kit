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
    # @todo если количество аккаунтов большое, то при тесте с дорогими функциями контракта падают потоки
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
        # ["0x1c3b9974c14381c932506742a79295a779307101",
        #  "68c83226fab45601676192434e7755073ce9a21f60485fc5edcd534614a15dfb"],     # 1 2 3
        # ["0x49d80828f56779f7ffc83114dfd7ce0aa9ce811c",
        #  "390527faae26b21a32e8f220919ae9af626f6f09a20013ae1b960297ea36ddcc"],     # 123
        # ["0x1f642cdc8ee32f586478bc7d5f14303f0fc0115d",
        #  "388fd455f5d3d785a7dce044f6cb60055a3cb4c282401d0b8dfc69c8ec7233aa"],     # 456
        ["0x8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2",
         "6d2f23ea27162fbb170f97b4840a272239be8b8d20c86b76f8e9d9193083546b"],     # 789
        # ["0xc464e62D62F9d95d7d1b3A963151389671Fe782b"],
        # ["0x5C954Fba7Df989C0DDa96eB7D7c861Ce9dd669b3"],
    )
    tests = TestController(WEB3_PROVIDER_URI, infura_config)

                                                    # Tests

    # tests.add_test("accounts")

    # tests.add_test("private", ("UTC--2018-12-03T14-59-13.944525811Z--1c3b9974c14381c932506742a79295a779307101", "1 2 3"))
    # tests.add_test("private", ("UTC--2018-12-03T15-01-03.047917914Z--49d80828f56779f7ffc83114dfd7ce0aa9ce811c", "123"))
    # tests.add_test("private", ("UTC--2018-12-03T15-08-09.573673621Z--1f642cdc8ee32f586478bc7d5f14303f0fc0115d", "456"))
    # tests.add_test("private", ("UTC--2018-12-03T15-08-28.053421410Z--8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2", "789"))


    # tests.add_test("new_acc", ("123", "390527faae26b21a32e8f220919ae9af626f6f09a20013ae1b960297ea36ddcc"))
    # tests.add_test("deploy", ("test.sol", accounts[0][1]))

    # tests.add_test("unlock", ("0x1c3b9974c14381c932506742a79295a779307101", "123"))
    # tests.add_test("unlock", ("0x49d80828f56779f7ffc83114dfd7ce0aa9ce811c", "1 2 3"))
    # tests.add_test("unlock", ("0x1f642cdc8ee32f586478bc7d5f14303f0fc0115d", "456"))
    # tests.add_test("unlock", ("0x8484aaf2eb9d16ddeaf8c05e0ac5d46fbd8410c2", "789"))

    # tests.add_test("send", (accounts[1][1], "0x8E4Fca6b50bB1f3D874bdda1F57D957868938ED1", "cycle", "test.abi"))

    # tests.add_test("get_trans", ("0xe16ab2cd31c17ef38154b0a340724eb44c505907916416b4e6805ee6805c258d", ))

    # for account in accounts:
    #     tests.add_test("balance", (account[0], ))

    # tests.add_test("test_many", (1,), accounts=accounts)
    # tests.add_test("send_eth", (accounts[0], accounts[1], 9998279548159572706035443367))
    # tests.add_test("test_expensive", (5,), accounts=accounts)

    tests.add_test("test_heavy", (10, "0xa529799148956751756F8EB4A414B0F959A1f96F", "empty", "test.abi"), accounts=accounts)
    # tests.add_test("test_heavy", (1, "0x038c7623c7a9d730170297De7B4d33Bb99dF98eD", "empty", "test.abi"), accounts=accounts) # ganache

    # tests.add_test("sametrans", (accounts, ))

    tests.start_tests()
