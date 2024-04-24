from fastapi import FastAPI
from src.db_stuff.config import engine, Base
from src.routes import asymmetric, symmetric

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(symmetric.router)
app.include_router(asymmetric.router)


@app.get("/")
def root():
    """
    Return list of avaible endpoints.
    """
    return {
        "Avaible endpoints": {
            "GET": {
                "/symetric/key": "Return randomly generated symmetric key",
                "/asymetric/key": "",
                "/asymetric/key/ssh": ""
            },
            "POST": {
                "/symetric/key": "Sets symmetric key on the server",
                "/symetric/encode": "Encrypts message using currently set symmetric key",
                "/symetric/decode": "Decrypts message using currently set symmetric key",
                "/asymetric/key": "",
                "/asymetric/verify": "",
                "/asymetric/sign": "",
                "/asymetric/encode": "",
                "/asymetric/decode": ""
            }
        }
    }
