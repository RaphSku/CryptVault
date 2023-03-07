from fastapi.testclient import TestClient

from cryptvault.vault   import Secret
from cryptvault.main    import cryptvault_server
from ..fixtures         import secret_key, secrets
from ..utilities        import startup, cleanup_base_path


client = TestClient(cryptvault_server)


class TestGetRouter:
    def test_get_s01(self, secret_key: str, secrets: list[Secret]):
        startup(secret_key = secret_key, secrets = secrets)

        guid    = 'test_secret_key'
        context = 'test'
        key     = 'key1'
        response = client.get(url = f"/cryptvault?guid={guid}&context={context}&key={key}")

        content  = response.json()

        assert response.status_code == 200
        assert content['key'] == 'key1'
        assert content['value'] == 'value1'

        cleanup_base_path()