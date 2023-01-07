from cryptvault.vault import Secret
from cryptvault.vault import encrypt_secrets, decrypt_secret

from ..fixtures import secrets, secret_key


class TestEncryption:
    def test_encryption_s01(self, secret_key: str, secrets: list[Secret]):
        encrypted_secrets = encrypt_secrets(in_secrets = secrets, secret_key = secret_key)

        is_bytes        = []
        number_of_bytes = []
        for encrypted_secret in encrypted_secrets:
            is_bytes.append(isinstance(encrypted_secret.value, bytes))
            number_of_bytes.append(len(encrypted_secret.value))

        assert all(is_bytes) == True
        assert number_of_bytes == [34, 34]


    def test_decryption_s01(self, secret_key: str, secrets: list[Secret]):
        encrypted_secrets = encrypt_secrets(in_secrets = secrets, secret_key = secret_key)

        decrypted_secrets = []
        for encrypted_secret in encrypted_secrets:
            decrypted_secrets.append(decrypt_secret(secret = encrypted_secret, secret_key = secret_key))

        for index in range(len(decrypted_secrets)):
            assert decrypted_secrets[index].key == secrets[index].key
            assert decrypted_secrets[index].value == secrets[index].value