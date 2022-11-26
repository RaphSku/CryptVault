from fastapi import APIRouter, Body

from cryptvault.vault import Registry, InSecrets, create_hashed_secret_key


post_router = APIRouter()

@post_router.post("/cryptvault")
async def addSecrets(secret_in: InSecrets = Body(embed = False)):
    guid    = secret_in.guid
    context = secret_in.context
    secrets = secret_in.secrets

    hashed_secret_key = create_hashed_secret_key(guid)

    registry   = Registry(context = context, secret_key = hashed_secret_key)
    registry.store_secrets(secrets)

    return {'message': 'Encryption of Secrets was successful'}