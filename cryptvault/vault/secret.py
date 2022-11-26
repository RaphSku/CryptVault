from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Secret:
    key: str
    value: str


@dataclass
class EncryptedSecret:
    key: str
    value: bytes


class InSecrets(BaseModel):
    guid: str
    context: str
    secrets: list[Secret]


class RequestSecret(BaseModel):
    guid: str
    context: str
    key: str