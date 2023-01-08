from fastapi.testclient import TestClient
from ..fixtures         import secrets
from ..utilities        import cleanup_base_path

from cryptvault.main    import cryptvault_server


client = TestClient(cryptvault_server)

class TestPostRouter:
    def test_post_s01(self, secrets):
        body     = {
            'guid': 'c210e426-c917-4fb1-8ae8-77331f69567e',
            'context': 'test',
            'secrets': [
                {'key': secrets[0].key, 'value': secrets[0].value},
                {'key': secrets[1].key, 'value': secrets[1].value}
            ]
        }
        response  = client.post(url = "/cryptvault", 
                                headers = {'Content-Type': 'application/json'},
                                json = body)
        content   = response.json()

        assert response.status_code == 200
        assert content == {'message': 'Encryption of Secrets was successful'}

        cleanup_base_path()