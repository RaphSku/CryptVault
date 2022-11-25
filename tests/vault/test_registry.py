import pytest
import os
import re
import base64
import pandas as pd
import pyarrow.parquet as pq

from cryptvault.vault import (
    Registry, 
    Secret, 
    EncryptedSecret,
    create_hashed_secret_key, 
    encrypt_secrets, 
    decrypt_secret
)


@pytest.fixture()
def get_encrypted_secrets():
    secret_key        = "test"
    secrets           = [Secret(key = "key1", value = "value1"), Secret(key = "key2", value = "value2")]
    hashed_secret_key = create_hashed_secret_key(secret_key)
    encrypted_secrets = encrypt_secrets(in_secrets = secrets, hash_secret_key = hashed_secret_key)

    return encrypted_secrets


class TestRegistry:
    def test_initialisation_s01(self):
        secret_key        = "test"
        hashed_secret_key = create_hashed_secret_key(secret_key)
        registry = Registry(path = "./", context = "test", hash_secret_key = hashed_secret_key)

        assert registry.context == "test"
        assert registry.hash_secret_key == hashed_secret_key
        assert registry.path == "./"


    def test_storing_secrets_s01(self, get_encrypted_secrets: list[EncryptedSecret]):
        secret_key        = "test"
        hashed_secret_key = create_hashed_secret_key(secret_key)
        registry          = Registry(path = "./", context = "test", hash_secret_key = hashed_secret_key)

        registry.store_secrets(encrypted_secrets = get_encrypted_secrets)

        with open('./logs/test/path.txt', 'r') as file:
            content        = file.read()
            act_context    = re.findall(r"(?=.*)\w*(?=-)", content)[0]
            act_secret_key = base64.b64decode(re.findall(r"(?=-).*", content)[0][1:])

        assert act_context    == "test"
        assert act_secret_key == hashed_secret_key

        all_files_exist = True
        if not os.path.exists("./test/secrets.parquet"):
            all_files_exist = False

        if not os.path.exists("./logs/test/path.txt"):
            all_files_exist = False

        os.remove("./test/secrets.parquet")
        os.remove("./logs/test/path.txt")
        os.rmdir("./test")
        os.rmdir("./logs/test")
        os.rmdir("./logs")

        assert all_files_exist == True


    def test_storing_secrets_s02(self, get_encrypted_secrets: list[EncryptedSecret]):
        secret_key        = "test"
        hashed_secret_key = create_hashed_secret_key(secret_key)
        registry          = Registry(path = "./", context = "test", hash_secret_key = hashed_secret_key)

        registry.store_secrets(encrypted_secrets = get_encrypted_secrets)

        with open('./logs/test/path.txt', 'r') as file:
            content        = file.read()
            act_context    = re.findall(r"(?=.*)\w*(?=-)", content)[0]
            act_secret_key = base64.b64decode(re.findall(r"(?=-).*", content)[0][1:])

        table = pq.read_table("test/secrets.parquet")
        df    = table.to_pandas()

        encrypted_secret_one = EncryptedSecret(key = get_encrypted_secrets[0].key, value = df[get_encrypted_secrets[0].key].iloc[0])
        act_secret_one       = decrypt_secret(secret = encrypted_secret_one, hash_secret_key = hashed_secret_key)

        encrypted_secret_two = EncryptedSecret(key = get_encrypted_secrets[1].key, value = df[get_encrypted_secrets[1].key].iloc[0])
        act_secret_two       = decrypt_secret(secret = encrypted_secret_two, hash_secret_key = hashed_secret_key)
        
        assert act_secret_one.value == "value1"
        assert act_secret_two.value == "value2"

        all_files_exist = True
        if not os.path.exists("./test/secrets.parquet"):
            all_files_exist = False

        if not os.path.exists("./logs/test/path.txt"):
            all_files_exist = False

        os.remove("./test/secrets.parquet")
        os.remove("./logs/test/path.txt")
        os.rmdir("./test")
        os.rmdir("./logs/test")
        os.rmdir("./logs")

        assert all_files_exist == True
