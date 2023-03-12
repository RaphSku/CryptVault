import os
import attrs
import uuid
import requests

from cryptvault.vault import Secret


@attrs.define()
class Client:
    host: str = attrs.field(factory = str)
    port: str = attrs.field(factory = str)

    def __init__(self, host: str, port: str, tls: bool) -> None:
        self.host = host
        self.port = port
        self.tls  = tls

        self.__create_guid()


    def get_secret(self, context: str, key: str) -> tuple[str, int]:
        base_url = f"http://{self.host}:{self.port}/cryptvault"
        if self.tls:
            base_url = f"https://{self.host}:{self.port}/cryptvault"

        guid_path = os.path.expanduser('~/.cryptvault/guid')
        with open(guid_path, 'r') as file:
            guid = file.read()
        response = requests.get(url = f"{base_url}?guid={guid}&context={context}&key={key}")
        content  = response.json()

        return content["value"], response.status_code


    def post_secrets(self, guid: str, context: str, secrets: list[Secret]) -> int:
        base_url = f"http://{self.host}:{self.port}/cryptvault"
        if self.tls:
            base_url = f"https://{self.host}:{self.port}/cryptvault"
        response = requests.post(url = f"{base_url}", 
                                 json = {
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