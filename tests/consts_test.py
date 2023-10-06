import consts as consts


def test_key():
    assert (
        consts.KEY == "1bd171c9e4c7831ace3c358d9c93ba3cc0304728d90a243830428a2c0dabfead"
    )


def test_secret():
    assert (
        consts.SECRET
        == "787a28958d7d9ce9e189527b2b4d8a4b608c8474d6447a23c3c88d9ff81c1269"
    )


def test_base_url():
    assert consts.BASE_URL == "https://testnet.binancefuture.com"
