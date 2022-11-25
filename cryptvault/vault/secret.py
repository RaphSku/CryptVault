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
    context: str
    secrets: list[Secret]