from fastapi import FastAPI

app = FastAPI()


@app.get("/symmetric/key")
def get_sym_key():
    return {"message": "Hello World"}


@app.post("/symmetric/key")
def set_sym_key():
    return {"message": "Hello World"}


@app.post("/symmetric/encode")
def sym_encode():
    return {"message": "Hello World"}


@app.post("/symmetric/decode")
def sym_decode():
    return {"message": "Hello World"}