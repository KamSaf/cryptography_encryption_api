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
                "/asymmetric/key": "",
                "/asymmetric/key/ssh": ""
            },
            "POST": {
                "/symmetric/key": "Sets symmetric key on the server",
                "/symmetric/encode": "Encrypts message using currently set symmetric key",
                "/symmetric/decode": "Decrypts message using currently set symmetric key",
                "/asymmetric/key": "",
                "/asymmetric/verify": "",
                "/asymmetric/sign": "",
                "/asymmetric/encode": "",
                "/asymemtric/decode": ""
            }
        }
    }
