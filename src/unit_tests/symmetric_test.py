from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.main import app, Base
from src.db_stuff.models import SymmetricKey
from sqlalchemy import select
from src.db_stuff.utils import get_db
from sqlalchemy.pool import StaticPool
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TESTING_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TESTING_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestAuth:

    def test_post_sym_encode_no_set_key(self):
        MESSAGE = "this is testing message"
        URL = "/symmetric/encode"
        response = client.post(url=URL, json={"message": MESSAGE})
        assert response.status_code == 422

    def test_post_sym_decode_no_set_key(self):
        MESSAGE = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/decode"
        response = client.post(url=URL, json={"message": MESSAGE})
        assert response.status_code == 422

    def test_post_sym_encode(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/key"
        add_key_response = client.post(url=URL, json={"key": HEX_KEY})
        assert add_key_response.status_code == 200
        MESSAGE = "this is testing message"
        URL = "/symmetric/encode"
        response = client.post(url=URL, json={"message": MESSAGE})
        assert response.status_code == 200
        encoded_msg = response.json()["encrypted message"]
        hex_msg = encoded_msg[:-32]
        hex_iv = encoded_msg[-32:]
        key = bytes.fromhex(HEX_KEY)
        iv = bytes.fromhex(hex_iv)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decr_msg = decryptor.update(bytes.fromhex(hex_msg)) + decryptor.finalize()
        assert decr_msg.rstrip(b"\0").decode() == MESSAGE

    def test_post_sym_encode_no_message(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/key"
        add_key_response = client.post(url=URL, json={"key": HEX_KEY})
        assert add_key_response.status_code == 200
        URL = "/symmetric/encode"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_sym_decode(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/key"
        add_key_response = client.post(url=URL, json={"key": HEX_KEY})
        assert add_key_response.status_code == 200
        ENCR_MESSAGE = "b25ea69ea9d1711a8d8577d481ca431e32600f81befb3e246ada6b153944b6ef09fd27397adfdaff5624cd077e880a77"
        MESSAGE = "this is testing message"
        URL = "/symmetric/decode"
        response = client.post(url=URL, json={"message": ENCR_MESSAGE})
        assert response.status_code == 200
        decr_msg = response.json()["decrypted message"]
        assert decr_msg == MESSAGE

    def test_post_sym_decode_no_message(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/key"
        add_key_response = client.post(url=URL, json={"key": HEX_KEY})
        assert add_key_response.status_code == 200
        URL = "/symmetric/decode"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_sym_key(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49"
        URL = "/symmetric/key"
        response = client.post(url=URL, json={"key": HEX_KEY})
        db = TestingSessionLocal()
        stmt = select(SymmetricKey.key).order_by(SymmetricKey.create_date.desc())
        result = db.execute(stmt).first()
        db.close()
        assert result is not None
        assert result[0] == HEX_KEY
        assert response.status_code == 200

    def test_post_sym_key_no_data(self):
        URL = "/symmetric/key"
        response = client.post(url=URL)
        assert response.status_code == 400

    def test_post_sym_key_data_too_long(self):
        HEX_KEY = "039ffd91f85570a439c14a30a27c23df660c7ce9c35876d5bf9b88753927ef49 AAA"
        URL = "/symmetric/key"
        response = client.post(url=URL, json={"key": HEX_KEY})
        assert response.status_code == 422

    def test_post_sym_key_data_too_short(self):
        HEX_KEY = "111"
        URL = "/symmetric/key"
        response = client.post(url=URL, json={"key": HEX_KEY})
        assert response.status_code == 422

    def test_get_sym_key(self):
        EXPECTED_KEY_LENGTH = 64
        URL = "/symmetric/key"
        response = client.get(url=URL)
        gen_key = response.json()["generated key"]
        assert response.status_code == 200
        assert type(gen_key) is str
        assert len(gen_key) == EXPECTED_KEY_LENGTH


if __name__ == "__main__":
    pass
