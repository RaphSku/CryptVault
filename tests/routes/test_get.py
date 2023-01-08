import os
import base64
import pyarrow
import pyarrow.parquet as pq
import pandas as pd

from fastapi.testclient import TestClient

from cryptvault.vault   import Secret, encrypt_secrets
from cryptvault.main    import cryptvault_server
from ..fixtures         import secret_key, secrets
from ..utilities        import cleanup_base_path


client = TestClient(cryptvault_server)

def startup(secret_key: str, secrets: list[Secret]):
    base_path = os.path.expanduser("~/cryptvault")
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

class TestGetRouter:
    def test_get_s01(self, secret_key: str, secrets: list[Secret]):
        startup(secret_key = secret_key, secrets = secrets)

        body = {
            'guid': 'test_secret_key',
            'context': 'test',
            'key': 'key1'
        }
        response = client.get(url = "/cryptvault", 
                              headers = {'Content-Type': 'application/json'},
                              params = body)

        content  = response.json()

        assert response.status_code == 200
        assert content['key'] == 'key1'
        assert content['value'] == 'value1'

        cleanup_base_path()