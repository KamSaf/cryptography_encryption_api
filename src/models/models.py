from pydantic import BaseModel


class NewSymmetricKey(BaseModel):
    key: str | None = None


class Message(BaseModel):
    message: str | None = None


if __name__ == "__main__":
    pass
