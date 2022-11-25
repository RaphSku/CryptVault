import os
import base64
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

from pathlib import Path 

from cryptvault.vault import Secret


class Registry:
    path_to_log: Path = Path('./logs')

    def __init__(self, path: Path, context: str, hash_secret_key: bytes) -> None:
        self.path            = path
        self.context         = context
        self.hash_secret_key = hash_secret_key


    def store_secrets(self, encrypted_secrets: list[Secret]):
        base_dir   = f'{self.path}'
        target_dir = f'{self.path}/{self.context}'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        secrets_in = {}
        for secret in encrypted_secrets:
            secrets_in[secret.key] = secret.value

        df_secrets = pd.DataFrame(data = secrets_in, index = ["value"])
        table      = pyarrow.Table.from_pandas(df_secrets)

        pq.write_table(table, f'{target_dir}/secrets.parquet')

        self.__create_registry_entry(target_dir)


    def __create_registry_entry(self, target_dir: str):
        if not os.path.exists(self.path_to_log):
            os.mkdir(self.path_to_log)

        if not os.path.exists(f"{self.path_to_log}/{self.context}"):
            os.mkdir(f"{self.path_to_log}/{self.context}")

        with open(f'{self.path_to_log}/{self.context}/path.txt', 'w') as file:
            file.write(f"{target_dir}-")
            file.write(base64.b64encode(self.hash_secret_key).decode('utf-8'))
            