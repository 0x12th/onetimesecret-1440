from typing import Annotated

from pydantic import BaseModel, Field


class SecretGenerateIn(BaseModel):
    secret_message: str
    passphrase: str
    ttl: Annotated[int, Field(gt=0, default=3600)] | None = None


class SecretGenerateOut(BaseModel):
    secret_key: str


class SecretGetIn(BaseModel):
    passphrase: str


class SecretGetOut(BaseModel):
    secret_message: str
