import os
import attrs
import uuid
import requests
import json


@attrs.define()
class Client:
    host: str = attrs.field(factory = str)
    port: str = attrs.field(factory = str)

    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

        self.__create_guid()


    def get_secret(self, context: str, key: str):
        with open('~/.cryptvault/guid', 'r') as file:
            guid = file.read()
        response = requests.get(url = f"{self.host}:{self.port}/cryptvault",
                        data = {
                            'guid': guid,
                            'context': context,
                            'key': key
                        })

        content  = json.loads(response.json())
        print(content)

    
    def __create_guid(self):
        if not os.path.exists("~/.cryptvault/guid"):
            guid = f"{uuid.uuid1()}-{uuid.uuid4()}"
            with open('~/.cryptvault/guid', 'w') as file:
                file.write(guid)