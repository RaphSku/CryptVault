import uuid

from fastapi import APIRouter, Body
from pathlib import Path

from cryptvault.vault import Registry, InSecrets, create_hashed_secret_key, encrypt_secrets


post_router = APIRouter()

@post_router.post("/cryptvault")
async def addSecrets(path: Path, secret_in: InSecrets = Body(embed = False)):
    context = secret_in.context
    secrets = secret_in.secrets

    guid = uuid.uuid1()
    with open(f'{path}/guids.txt', 'w') as file:
        file.write(f"{context}:{guid}")

    hash_secret_key = create_hashed_secret_key(f"{context}{guid}")
    encrypt_secrets(secrets, hash_secret_key)

    registry = Registry(path = path, context = context, hash_secret_key = hash_secret_key)
    registry.store_secrets(secrets)

    return {'message': 'Encryption of Secrets was successful'}