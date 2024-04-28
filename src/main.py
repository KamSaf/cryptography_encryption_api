from fastapi import FastAPI
from src.db_stuff.config import engine, Base
from src.routes import asymmetric, symmetric

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(symmetric.router)
app.include_router(asymmetric.router)


@app.get("/")
def root() -> dict:
    """
    Return list of avaible endpoints.
    """
    return {
        "Avaible endpoints": {
            "GET": {
                "/symmetric/key": "Return randomly generated symmetric key",
                "/asymmetric/key": "Returns new private and public asymmetric keys and sets them on the server",
                "/asymmetric/key/ssh": "Returns new private and public asymmetric keys in an OpenSSH format"
            },
            "POST": {
                "/symmetric/key": "Sets symmetric key on the server - Parameters: key",
                "/symmetric/encode": "Encrypts message using currently set symmetric key - Parameters: message",
                "/symmetric/decode": "Decrypts message using currently set symmetric key - Parameters: message",
                "/asymmetric/key": "Sets private and public asymmetric keys on the server - Parameters: public_key, private_key",
                "/asymmetric/sign": "Signs given message with currently set private RSA key - Parameters: message",
                "/asymmetric/verify": "Verifies signature on a given message - Parameters: message, signature",
                "/asymmetric/encode": "Encrypts and returns given message using currently set RSA public key - Parameters: message",
                "/asymemtric/decode": "Decrypts and returns given message using currently set RSA private key - Parameters: message",
            }
        }
    }
