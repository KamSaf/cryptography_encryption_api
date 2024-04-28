from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.main import app, Base
from src.db_stuff.utils import get_db
from sqlalchemy.pool import StaticPool

TESTING_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TESTING_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

EXAMPLE_PUBLIC_KEY = "30820122300d06092a864886f70d01010105000382010f003082010a02820101009e341352b9e932e1595feddcd935fc695841d7130f230e42c6d255e67748626d9ebf967685091e159be1b51037621084943af86c74ae0a2adddb56ae5e61f1780de42337fe93bda545d48b0bb301b550bd1dc0588a1d0196c0fa3596f3055ba07bcf9e5640703b06d004dcb81cec7046cfd970622488736dcd7acb5ece1143c690982aa618e961dc152ddadee6c85a459e014575458287a68ead47bb777d260fda0b90ebd2f3b8d99511ad091c401db8d14063ed429c6ff32c49e2b74a1986ef9e22ca03233b93421677d54886c07d460bbb873f0f1985d3109ba2cef966d113ff117f5fc602e8c324836c8c85ec6cb771d699051db0353398f11ff9a6d17aa70203010001"
EXAMPLE_PRIVATE_KEY = "30820535305f06092a864886f70d01050d3052303106092a864886f70d01050c30240410c9ec467fe96c65142a339d7bdc0ecc6f02020800300c06082a864886f70d02090500301d060960864801650304012a04100416a17f93bb7e12a1002ed881484567048204d0090cafc70c75c24db159656b5639828bfb44ad221dc6919904a294c66694708317d7472fa81301b2d0d22b7ffb007bc35d57041a8d7120dcd0168ce057cf162775df57dba86afbf005742875a862c1442ea3081236e2596be8a8377571d7fead1b713e79d4e2463c501c36f4eda5434f312f18531825d1218b7d440be99af2514edb357ea45cc3c80fa69a45764b3d8d88cc986bb4608a42b6b3c313e2ee56b44b6848f7fd09d789bba67552b5b7d04a8d3c0cd51dfcee6934a20681e0f1420773831564e526ce7c2a9b7df3678f2f2be37c568aa3090e67611154867f7001285f54fc0b684269c7bd67cca5c668e9852d496103a41e78e2c049ea2aed8b95c3ad2c4da7ac33ec4f84f2a93e51655ded9a80cc4eb23c6b65929fbc8143bd93030385c9f49ba3b7c6e433c201a4f14de0df4032803f443dd90114c91a2245adf7b0d867704c12ead070043ab80778ebcd62cb0f08f12c17c25a7ff84b615b1228413f08e6bdfa87549f1453b7a5e59a433cf4f6c5773062aead61ba45c7a2c9a0b444a4b651000671d44881d07dd7aa936ab866a1b262e10460eca75fb9411143badb27ac26a301d07c650ec38e0f4159484d24bf8bbe02a332377b2964e9332659155bc5748a3fae1c29b83b77a0da7bf6419c93ba644b451798b73021b1ad980e81e7636c9776b940351aae2e23435d731475534bc3ac68804bf6a55194584625018c8f8b49421857e264c7a49a9805d79d748f5ff557a82c0f9c4670529044ba5228d8b2d53fc392dce9a9ee515b7dc38c640144e434b7fac9fd10413d1f0c684cb46549dc5cbf60a99e4b9460b9a171761c16084fb473b83dfc7236e3134be4c2d957cf116c29b7594ad518d036d34be31efb99d46454db452c13e1947f76eadff68ecdecfed0400708798172c9d2f6db729ea31007b3d690adb3917f49d4d28fa630cdf98b746434f71a4cb20cdd31cb16d89427b0938c0e59e794f377d481ae06006756f6a4ebe3bb9120bfa6e8f85542ed6fff0eb0308d0204ae4589451a9bb39081d175afb9e0ce995c073f857dc0056e959169cb992c8b983ecf4048e4a27eaf6780ca5308c48587d3c8b5b1c576566e8eea5f701c26402ee05dd2aa5bf7d30d9554f3d706880613266b586c306cb5b79abebd1d3146d051e7f4b47dd1ff058b163a2d6a63682ad2ac8de8126f0d407f889a325ee4be72c9e83d16eeaf549d0b5d37aefdd1fe45ed72d83bbec8e865fba5d863737476ee3c2f95c01a33aae843b421a1af6cac1fd26d511f98da83471799679ff15b2516e469a6b028fbe3c34425e403bc3656dc4256b1332cfd0a3acbe54905f7073b824d849fd531a5488b953144baca07d83b091ef9c7c26dd7c8a8524c28dd40e52484722e9d7d485f9c450f4e8cd8d186e7c45a84fdf794befc6d5b670595fc70b00d32497f10f79a226ceec281102bf026a2fa7c476db4d33d12ce9543a25cfb6ca61752a18664edf1eefd8cf2d171bd046e7f84bac40ef1779b813f4caa9cd1581ab50594ecc2a0a8f31735b9b3135a7212fb2aad9c266f094fd3b008306e1097f7a907590d172bb217aca7d617e2f202d9ab700435c762bf695cdb04075ff4aa059172954ed67b57417cbf25c431993583b3b12a8f2c379dacdd88df30b8100e105f209bd963049da474254c62add0810d641fdeca8b03be7f2357bdb817c82bdee0a9ed554bee93bd9f091f9b0892542ef8d2636c"
EXAMPLE_MESSAGE = "this is testing message"
EXAMPLE_SIGNATURE = "46200189e3c3b0d4e36310a9eb945b63c86e7df16b6a2872dc37be1bc9c6146e799a9325de66948ef4b4d57732aed7f481a10db2a4f30067b1c4764bcaac38f9e2b6b470e9a7f4401145af451896b021e2e0ba26da6a5fc598ef5b15c4e4aabb6487a0db10b8022e7f4b9cda241dd6d4d1d981e11e04e593b0f8b5b9bb86ddda2189914b3b70a2ffe4daa4976807446294498a871f6cb862088aedb12b96fed16a545fdb97bfc14437c0b01f0ee7cad417ac3753f898cef74fd7706ef41e6f60e13d391b22623384fdc5bf9d23ec111148abd0438b92d52c6e421a69217b380e0b2afa51db7e4fb7fb3c1c6af4449bab989bfe47911dfdcdfbfecdc7911c293f"


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestAsymmetricRoutes:

    def test_get_asym_key(self):
        URL = "/asymmetric/key"
        response = client.get(url=URL)
        keys = list(response.json().keys())
        assert len(response.json().values()) == 2
        assert keys[0] == "public_key"
        assert keys[1] == "private_key"
        assert response.status_code == 200

    def test_get_key_ssh(self):
        URL = "/asymmetric/key/ssh"
        response = client.get(url=URL)
        keys = list(response.json().keys())
        assert len(response.json().values()) == 2
        assert keys[0] == "public_key_ssh"
        assert keys[1] == "private_key_ssh"
        assert response.status_code == 200

    def test_post_asym_key(self):
        URL = "/asymmetric/key"
        response = client.post(url=URL, json={"private_key": EXAMPLE_PRIVATE_KEY, "public_key": EXAMPLE_PUBLIC_KEY})
        assert response.status_code == 200

    def test_post_asym_key_no_data(self):
        URL = "/asymmetric/key"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_asym_key_no_private_key(self):
        URL = "/asymmetric/key"
        response = client.post(url=URL, json={"public_key": EXAMPLE_PUBLIC_KEY})
        assert response.status_code == 400

    def test_post_asym_key_no_public_key(self):
        URL = "/asymmetric/key"
        response = client.post(url=URL, json={"private_key": EXAMPLE_PRIVATE_KEY})
        assert response.status_code == 400

    def test_post_asym_sign(self):
        SET_KEYS_URL = "/asymmetric/key"
        response = client.post(url=SET_KEYS_URL, json={"private_key": EXAMPLE_PRIVATE_KEY, "public_key": EXAMPLE_PUBLIC_KEY})
        assert response.status_code == 200
        URL = "asymmetric/sign"
        response = client.post(url=URL, json={"message": EXAMPLE_MESSAGE})
        keys = list(response.json().keys())
        values = list(response.json().values())
        assert response.status_code == 200
        assert len(values) == 2
        assert len(keys) == 2
        assert keys[0] == "message"
        assert keys[1] == "signature"
        assert values[0] == EXAMPLE_MESSAGE

    def test_post_asym_sign_no_message(self):
        URL = "asymmetric/sign"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_asym_verify(self):
        SET_KEYS_URL = "/asymmetric/key"
        response = client.post(url=SET_KEYS_URL, json={"private_key": EXAMPLE_PRIVATE_KEY, "public_key": EXAMPLE_PUBLIC_KEY})
        assert response.status_code == 200
        SIGN_MESSAGE_URL = "/asymmetric/sign"
        response = client.post(url=SIGN_MESSAGE_URL, json={"message": EXAMPLE_MESSAGE})
        assert response.status_code == 200
        signature = response.json()["signature"]
        URL = "asymmetric/verify"
        response = client.post(url=URL, json={"message": EXAMPLE_MESSAGE, "signature": signature})
        keys = list(response.json().keys())
        values = list(response.json().values())
        assert response.status_code == 200
        assert len(values) == 1
        assert len(keys) == 1
        assert keys[0] == "detail"
        assert values[0] is True

    def test_post_asym_verify_invalid_signature(self):
        SET_KEYS_URL = "/asymmetric/key"
        response = client.post(url=SET_KEYS_URL, json={"private_key": EXAMPLE_PRIVATE_KEY, "public_key": EXAMPLE_PUBLIC_KEY})
        assert response.status_code == 200
        URL = "asymmetric/verify"
        WRONG_SIGNATURE = b"wrong signature".hex()
        response = client.post(url=URL, json={"message": EXAMPLE_MESSAGE, "signature": WRONG_SIGNATURE})
        keys = list(response.json().keys())
        values = list(response.json().values())
        assert response.status_code == 200
        assert len(values) == 1
        assert len(keys) == 1
        assert keys[0] == "detail"
        assert values[0] is False

    def test_post_asym_verify_no_data(self):
        URL = "asymmetric/verify"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_asym_verify_no_message(self):
        URL = "asymmetric/verify"
        response = client.post(url=URL, json={"signature": EXAMPLE_SIGNATURE})
        assert response.status_code == 400

    def test_post_asym_verify_no_signature(self):
        URL = "asymmetric/verify"
        response = client.post(url=URL, json={"message": EXAMPLE_MESSAGE})
        assert response.status_code == 400

    def test_post_asym_encode(self):
        URL = "asymmetric/encode"
        response = client.post(url=URL, json={"message": EXAMPLE_MESSAGE})
        assert response.status_code == 200
        keys = list(response.json().keys())
        values = list(response.json().values())
        assert response.status_code == 200
        assert len(values) == 1
        assert len(keys) == 1
        assert keys[0] == "encrypted_message"

    def test_post_asym_encode_no_message(self):
        URL = "asymmetric/encode"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_asym_decode(self):
        ENCODE_URL = "asymmetric/encode"
        encode_response = client.post(url=ENCODE_URL, json={"message": EXAMPLE_MESSAGE})
        assert encode_response.status_code == 200

        DECODE_URL = "asymmetric/decode"
        response = client.post(url=DECODE_URL, json={"message": encode_response.json()["encrypted_message"]})

        keys = list(response.json().keys())
        values = list(response.json().values())
        assert response.status_code == 200
        assert len(values) == 1
        assert len(keys) == 1
        assert keys[0] == "decrypted_message"
        assert values[0] == EXAMPLE_MESSAGE

    def test_post_asym_decode_no_message(self):
        ENCODE_URL = "asymmetric/decode"
        encode_response = client.post(url=ENCODE_URL)
        assert encode_response.status_code == 400


if __name__ == "__main__":
    pass
