import re
import pyarrow.parquet as pq

from fastapi import APIRouter

from cryptvault.vault import decrypt_secret


get_router = APIRouter()

@get_router.get("/cryptvault")
async def getSecret(context: str, key: str):
    with open(f'./logs/{context}/path.txt', 'r') as file:
        target = file.read()

    result = re.findall(".\/\w*", target)

    result2 = re.findall("b'.*", target)

    table = pq.read_table(f'{result[0][:-1]}/secrets.parquet')
    df = table.to_pandas()

    secret = df[key].iloc[0]

    return decrypt_secret(secret = secret, hash_secret_key = bytes(result2[0], encoding = 'utf-8'))


@get_router.get("/cryptvault/{context}")
async def getSecretsByContext(context: str):
    pass