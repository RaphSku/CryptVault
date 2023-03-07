import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from cryptvault.vault   import Secret
from cryptvault.main    import cryptvault_server
from cryptvault.client  import Client
from ..fixtures         import secret_key, secrets
from ..utilities        import startup, cleanup_base_path


client = TestClient(cryptvault_server)


class TestClientAssistent:
    def test_client_initalization_s01(self):
        base_path = os.path.expanduser("~/.cryptvault")
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        exp_host = "localhost"
        exp_port = "8000"
        client_assistant = Client(host = exp_host, port = exp_port)
        
        act_host = client_assistant.host
        act_port = client_assistant.port

        assert act_host == exp_host
        assert act_port == exp_port

        os.remove(f"{base_path}/guid")
        os.rmdir(base_path)


    def test_guid_file_creation_s01(self):
        base_path = os.path.expanduser("~/.cryptvault")
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        _ = Client(host = "localhost", port = "8000")

        guid_path = f"{base_path}/guid"
        assert os.path.exists(guid_path)

        with open(guid_path, 'r') as file:
            guid = file.read()
        
        assert guid != ""

        os.remove(f"{base_path}/guid")
        os.rmdir(base_path)


    def test_post_secrets_s01(self, secret_key: str, secrets: list[Secret]):
        startup(secret_key = secret_key, secrets = secrets)
        
        client_assistant = Client(host = "localhost", port = "8000")

        guid_path = os.path.expanduser('~/.cryptvault/guid')
        with open(guid_path, 'r') as file:
            guid = file.read()
        
        with patch(target = "requests.post") as Mock:
            Mock.return_value = client.post(
                url = "/cryptvault",
                headers = {'Content-Type': 'application/json'},
                json = {
                    'guid': guid,
                    'context': 'test',
                    'secrets': [{"key": secret.key, "value": secret.value} for secret in secrets]
            })
            status_code = client_assistant.post_secrets(guid = guid, context = "test", secrets = secrets)

        assert status_code == 200

        cleanup_base_path()


    def test_get_secrets_s01(self, secret_key: str, secrets: list[Secret]):
        startup(secret_key = secret_key, secrets = secrets)
        
        client_assistant = Client(host = "localhost", port = "8000")

        guid_path = os.path.expanduser('~/.cryptvault/guid')
        with open(guid_path, 'r') as file:
            guid = file.read()
        guid = 'test_secret_key'
        
        with patch(target = "requests.get") as Mock:
            context = 'test'
            Mock.return_value = client.get(url = f"/cryptvault?guid={guid}&context={context}&key={secrets[0].key}")
            act_value, act_status_code = client_assistant.get_secret(context = "test", key = "key1")

        assert act_status_code == 200
        assert act_value       == secrets[0].value

        cleanup_base_path()