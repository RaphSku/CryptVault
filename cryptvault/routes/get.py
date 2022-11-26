from fastapi import APIRouter, Body

from cryptvault.vault import decrypt_secret, create_hashed_secret_key, RegisterManager, RequestSecret


get_router = APIRouter()

@get_router.get("/cryptvault")
async def getSecret(request: RequestSecret = Body(embed = False)):
    guid = create_hashed_secret_key(request.guid)

    register_manager = RegisterManager()
    secret_key       = register_manager.get_secret_key(context = request.context)
    if secret_key != guid:
        return {'error': 'guid does not match...access denied'}

    encrypted_secret = register_manager.get_encrypted_secret(context = request.context, key = request.key)
    secret           = decrypt_secret(secret = encrypted_secret, secret_key = secret_key)

    return secret