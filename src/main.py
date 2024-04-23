from fastapi import FastAPI
from src.db_stuff.config import engine, Base
from src.routes import asymmetric, symmetric

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(symmetric.router)
app.include_router(asymmetric.router)
