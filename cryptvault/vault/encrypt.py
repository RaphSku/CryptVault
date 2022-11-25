import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from hashlib import blake2b

from cryptvault.vault import Secret, EncryptedSecret


def create_hashed_secret_key(key: str):
    hash_gen   = blake2b(digest_size = 32)
    hash_gen.update(bytes(key, encoding = 'utf-8'))

    return hash_gen.digest()


def encrypt_secrets(in_secrets: list[Secret], hash_secret_key: bytes) -> list[EncryptedSecret]:
    encrypted_secrets = []
    for secret in in_secrets:
        fresh_bytes  = secrets.token_bytes(nbytes = 12)
        cipher       = fresh_bytes + AESGCM(key = hash_secret_key).encrypt(fresh_bytes, bytes(f"{secret.value}", encoding = 'utf-8'), b"")
        encrypted_secrets.append(EncryptedSecret(key = secret.key, value = cipher))

    return encrypted_secrets


def decrypt_secret(secret: EncryptedSecret, hash_secret_key: bytes) -> Secret:
    decrypted_secret = AESGCM(key = hash_secret_key).decrypt(secret.value[:12], secret.value[12:], b"")

    return Secret(key = secret.key, value = str(decrypted_secret, encoding = 'utf-8'))