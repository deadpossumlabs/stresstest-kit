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
    WEB3_PROVIDER_URI = "HTTP://127.0.0.1:8545"
    # WEB3_PROVIDER_URI = "HTTP://104.248.67.155:8545"
    # WEB3_PROVIDER_URI = "HTTP://192.168.1.19:8545"
    # test1 = TestController(WEB3_PROVIDER_URI, infura_config)
    # test2 = TestController(WEB3_PROVIDER_URI, base_config)

    # lock1 = RLock()
    # lock2 = RLock()
    # @todo если количество аккаунтов большое, то при тесте с дорогими функциями контракта падают потоки
    accounts = (["0x6f01Df94aD13495c9CDe2dc2aE272e5e559834B4",
                 "f168194b09d855dcfee49d73f237ac3f26f3a5fbaff19f24af6283418f336eab"],
                ["0xfBfFaa86d30053418Eb5596334FAfE35415E8706",
                 "2d7faf62bdc964e8723f148b129c66723478fbbf05d8de41f39edc24bae581ed"],
                ["0x8bbbc4CD72Dd576ED731080d5cc36E411d9c326d",
                 "a9dc7f48730076af0e923bf4eb43ff459d78ad467247b3e66637b3e4cc913ab0"],
                ["0xFF66A2921b81FdeD548734b716cEA382ca0ec0E6",
                 "265d027ce739bd0e38d6c6842dcc54c5f0b576b9c85dd269ba1f4b533badc1f9"],
                # ["0x5867Afc85076C6243a74E4Fe2Ff4ea95719E293e",
                #  "be8aa0b785ab06756247f04e446fff526f8ede1864d172bc8db1eeaccc8f6c32"],
                # ["0xaf073f0849e779202d0A92a12128C3b144856D6f",
                #  "c8959bd1b6835f5a367697e7456655aa026009cbf17bbfe9c87c13ea3c1b8ac3"],
                # ["0x9c35Df66Fe1Df12831C1ECAd1983DA0aAefd6658",
                #  "86f7c68a91e7e6dbc6ad149faccf46783acadb64f5f0e1022b08b6923c43186f"],
                # ["0x5A2569dC467c30c76D7C1E54536fd15675654A1F",
                #  "8735cc620363abffe94f67c791c4a095d148e29e21e71f21fd3a902c177b8c4c"],
                # ["0xb28FF41AB43d14dfCBcD0D9135b420e667d69d1A",
                #  "e6b79ce756caae056bbc21519a7ad54f73d037250ddec5c5f884be89ff68cfde"],
                # ["0x425a394c5F54Ab037CdFd23e6A622Fe4c6cf8DC6",
                #  "2fe52627b246f5e3480a6c3a1cd5ce26341978a0b73f08a66c7a803cc29feedb"],
                )
    #
    # accounts = (
    #     ["0x002491c91e81da1643de79582520ac4c77229e58",
    #      "df3aa14f4f2863cb3fe9fcb3290bbc0d9b5f4c1a1886d2bf53577e841ad38624"],
    #     ["0x40fdee788a2b2cce016660fc5e7a3efeaaf0a860",
    #      "4B840E1D567A493B9B21308D2C85616C56CD664C97520B041F539EC5F35F62AA"],
    # )
    tests = TestController(WEB3_PROVIDER_URI, infura_config)

                                                    # Tests

    # tests.add_test("accounts")
    # tests.add_test("deploy", ("test.sol", accounts[1][1]))
    # tests.add_test("send", (accounts[1][1], "0x8E4Fca6b50bB1f3D874bdda1F57D957868938ED1", "cycle", "test.abi"))
    # tests.add_test("get_trans", ("0xe16ab2cd31c17ef38154b0a340724eb44c505907916416b4e6805ee6805c258d", ))
    # tests.add_test("balance", ("0x92942A44752A4840803ac4B51D6A6Fd5820d73cB", ))
    # tests.add_test("test_many", (20,), accounts=accounts)
    tests.add_test("test_expensive", (20,), accounts=accounts)

    # tests.add_test("test_heavy", (20, "0xb3E68acE495495eaB3fDE4aE421372bD099c2661", "empty", "test.abi"), accounts=accounts)

    # tests.add_test("sametrans", (accounts, ))

    tests.start_tests()
