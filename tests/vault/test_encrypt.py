import pytest

from cryptvault.vault import Secret, EncryptedSecret
from cryptvault.vault import create_hashed_secret_key, encrypt_secrets, decrypt_secret


class TestHashedSecret:
    def test_create_hashed_secret_key_s01(self):
        hashed_secret_key = create_hashed_secret_key("Testing")

        assert type(hashed_secret_key) == bytes
        assert len(hashed_secret_key) == 32
        assert hashed_secret_key == bytes(b'/\x8aE\xe3:A\xb7\xf4\xef/?2\xf7p\xc7\xd7u\xf51z\x90%l\xf9\xe5\xe2:5\xfc@\xb4\xb3')


@pytest.fixture()
def get_secrets():
    yield [Secret(key = "Key1", value = "Value1"), Secret(key = "Key2", value = "Value2")]


def assert_encrypted_secret(secret: EncryptedSecret, size: int):
    assert type(secret.value) == bytes
    assert len(secret.value) == size


class TestSecretEncryption:
    def test_encryption_secret_s01(self, get_secrets: list[Secret]):
        secret_key = "Test"
        hashed_secret_key = create_hashed_secret_key(secret_key)
        encrypted_secrets = encrypt_secrets(in_secrets = get_secrets, hash_secret_key = hashed_secret_key)

        for encrypted_secret in encrypted_secrets:
            assert_encrypted_secret(secret = encrypted_secret, size = 34)


class TestSecretDecryption:
    def test_decrypting_secret_s01(self, get_secrets: list[Secret]):
        secret_key = "Test"
        hashed_secret_key = create_hashed_secret_key(secret_key)
        encrypted_secrets = encrypt_secrets(in_secrets = get_secrets, hash_secret_key = hashed_secret_key)

        decrypted_secrets = []
        for encrypted_secret in encrypted_secrets:
            decrypted_secrets.append(decrypt_secret(secret = encrypted_secret, hash_secret_key = hashed_secret_key))

        assert len(decrypted_secrets[0].value) == 6
        assert type(decrypted_secrets[0].value) == str
        
        assert len(decrypted_secrets[1].value) == 6
        assert type(decrypted_secrets[1].value) == str