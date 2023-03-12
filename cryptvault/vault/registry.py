import os
import base64
import re
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

from pathlib import Path 

from cryptvault.vault.secret import Secret, EncryptedSecret
from cryptvault.vault.encrypt import encrypt_secrets


class RegisterHandle:
    base_path: Path = Path(os.path.expanduser("~/cryptvault"))


class RegisterManager(RegisterHandle):
    def __init__(self) -> None:
        self.registries = {}

        self.__parse_registries()

    
    def get_secret_key(self, context: str) -> bytes:
        with open(os.path.join(self.base_path, f"{context}.txt"), 'r') as file:
            secret_key = base64.b64decode(file.read())

        return secret_key


    def get_encrypted_secret(self, context: str, key: str) -> EncryptedSecret:
        df_encrypted_secret    = pq.read_table(self.registries[context], columns = [key]).to_pandas()
        encrypted_secret_value = df_encrypted_secret[key].iloc[0]

        return EncryptedSecret(key = key, value = bytes(encrypted_secret_value))

    
    def __parse_registries(self):
        files = os.listdir(f"{self.base_path}")

        registries = []
        for file in files:
            try:
                parquet_file = re.findall(".*.parquet", file)[0]
            except IndexError:
                continue
            registries.append(f"{self.base_path}/{parquet_file}")

        for registry in registries:
            regex_search = re.findall(r"\/.*(?=_secrets\.)", registry)[0]
            context      = regex_search.split("/")[-1]
            self.registries[context] = registry


class Registry(RegisterHandle):
    def __init__(self, context: str, secret_key: bytes) -> None:
        self.context = context

        self.__create_registry_directory()
        self.__store_secret_key(secret_key)


    def store_secrets(self, secrets: list[Secret]) -> None:
        with open(os.path.join(self.base_path, f"{self.context}.txt"), 'r') as file:
            secret_key = base64.b64decode(file.read())

        encrypted_secrets = encrypt_secrets(secrets, secret_key = secret_key)

        secrets_in = {}
        for encrypted_secret in encrypted_secrets:
            secrets_in[encrypted_secret.key] = encrypted_secret.value

        df_secrets = pd.DataFrame(data = secrets_in, index = ["value"])
        table      = pyarrow.Table.from_pandas(df_secrets)

        target_file = f'{self.base_path}/{self.context}_secrets.parquet'
        pq.write_table(table, target_file)


    def __store_secret_key(self, secret_key: bytes):
        with open(os.path.join(self.base_path, f"{self.context}.txt"), 'w') as file:
            file.write(base64.b64encode(secret_key).decode('utf-8'))


    def __create_registry_directory(self):
        self.base_path.mkdir()