from pydantic import BaseModel


class SetSymmetricKey(BaseModel):
    key: str
