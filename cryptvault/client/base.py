import os
import attrs
import uuid
import requests

from cryptvault.vault import Secret


@attrs.define()
class Client:
    host: str = attrs.field(factory = str)
    port: str = attrs.field(factory = str)

    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

        self.__create_guid()


    def get_secret(self, context: str, key: str) -> tuple[str, int]:
        guid_path = os.path.expanduser('~/.cryptvault/guid')
        with open(guid_path, 'r') as file:
            guid = file.read()
        response = requests.get(url = f"{self.host}:{self.port}/cryptvault?guid={guid}&context={context}&key={key}")
        content  = response.json()

        return content["value"], response.status_code


    def post_secrets(self, guid: str, context: str, secrets: list[Secret]) -> int:
        response = requests.post(url = f"{self.host}:{self.port}/cryptvault", data = {
            'guid': guid,
            'context': context,
            'secrets': [{"key": secret.key, "value": secret.value} for secret in secrets]
        })

        return response.status_code

    
    def __create_guid(self):
        base_path = os.path.expanduser('~/.cryptvault')
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        if not os.path.exists(f"{base_path}/guid"):
            guid      = f"{uuid.uuid1()}-{uuid.uuid4()}"
            guid_path = os.path.expanduser(f"{base_path}/guid")
            with open(guid_path, 'w') as file:
                file.write(guid)