import pytest

from cryptvault.vault import create_hashed_secret_key, Secret


@pytest.fixture()
def secret_key():
    SECRET_KEY = "test_secret_key"

    return create_hashed_secret_key(SECRET_KEY) 


@pytest.fixture()
def secrets() -> list[Secret]:
    secrets = []
    secrets.append(Secret(key = "key1", value = "value1"))
    secrets.append(Secret(key = "key2", value = "value2"))

    return secrets
