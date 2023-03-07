import os
import base64
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

from cryptvault.vault import Secret, encrypt_secrets


def startup(secret_key: str, secrets: list[Secret]):
    base_path = os.path.expanduser("~/cryptvault")
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    txt_file  = os.path.join(base_path, 'test.txt')
    with open(txt_file, 'w') as file:
        file.write(base64.b64encode(secret_key).decode('utf-8'))

    encrypted_secrets = encrypt_secrets(secrets, secret_key = secret_key)

    secrets_in = {}
    for encrypted_secret in encrypted_secrets:
        secrets_in[encrypted_secret.key] = encrypted_secret.value

    df_secrets = pd.DataFrame(data = secrets_in, index = ["value"])
    table      = pyarrow.Table.from_pandas(df_secrets)

    target_file = os.path.join(base_path, 'test_secrets.parquet')
    pq.write_table(table, target_file)


def cleanup_base_path():
    base_path = os.path.expanduser("~/cryptvault")
    os.remove(f"{base_path}/test_secrets.parquet")
    os.remove(f"{base_path}/test.txt")
    os.rmdir(f"{base_path}")