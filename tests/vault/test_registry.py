import os
import pyarrow.parquet as pq

from cryptvault.vault import (
    Registry, 
    RegisterManager,
    Secret, 
)
from ..fixtures import secrets, secret_key


def cleanup():
    base_path = os.path.expanduser("~/cryptvault")
    os.remove(f"{base_path}/test_secrets.parquet")
    os.remove(f"{base_path}/test.txt")
    os.rmdir(f"{base_path}")


class TestRegistry:
    def test_registry_initialisation_s01(self, secret_key: str):
        act_context = "test"
        registry    = Registry(context = act_context, secret_key = secret_key)

        assert registry.context == act_context


    def test_store_secrets_s01(self, secret_key: str, secrets: list[Secret]):
        registry  = Registry(context = "test", secret_key = secret_key)
        registry.store_secrets(secrets = secrets)

        df = pq.read_table("~/cryptvault/test_secrets.parquet").to_pandas()
        
        assert isinstance(df['key1'].value, bytes)
        assert isinstance(df['key2'].value, bytes)
        assert all(df.columns == ['key1', 'key2'])
        assert df.index.values[0] == 'value'

        cleanup()


    def test_store_secrets_s02(self, secret_key: str, secrets: list[Secret]):
        registry  = Registry(context = "test", secret_key = secret_key)
        registry.store_secrets(secrets = secrets)

        assert os.path.exists(f'{registry.base_path}/test.txt')

        cleanup()


class TestRegisterManager:
    def test_register_manager_initialisation_s01(self, secret_key: str, secrets: list[Secret]):
        registry  = Registry(context = "test", secret_key = secret_key)
        registry.store_secrets(secrets = secrets)

        register_manager = RegisterManager()
        
        assert register_manager.registries == {'test': f"{register_manager.base_path}/test_secrets.parquet"}

        cleanup()


    def test_register_manager_secret_key_retrieval_s01(self, secret_key: str, secrets: list[Secret]):
        registry  = Registry(context = "test", secret_key = secret_key)
        registry.store_secrets(secrets = secrets)

        register_manager = RegisterManager()
        secret_key = register_manager.get_secret_key(context = "test")

        assert isinstance(secret_key, bytes)

        cleanup()


    def test_register_manager_encrypted_secret_retrieval_s01(self, secret_key: str, secrets: list[Secret]):
        registry  = Registry(context = "test", secret_key = secret_key)
        registry.store_secrets(secrets = secrets)

        register_manager = RegisterManager()
        encrypted_secret = register_manager.get_encrypted_secret(context = "test", key = "key1")

        assert encrypted_secret.key == secrets[0].key
        assert isinstance(encrypted_secret.value, bytes)

        cleanup()