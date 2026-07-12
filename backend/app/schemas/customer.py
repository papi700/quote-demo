from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
