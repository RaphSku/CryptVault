import click
import uvicorn
import sys
import os

from fastapi import FastAPI

sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
import cryptvault.routes.get  as get
import cryptvault.routes.post as post


cryptvault_server = FastAPI()

cryptvault_server.include_router(get.get_router)
cryptvault_server.include_router(post.post_router)


@click.group()
def main():
    pass


@main.command()
@click.option('--host', '-h', default = "localhost", help = 'host on which the server should run')
@click.option('--port', '-p', default = "8000", help = 'port assigned to the server')
def start(host, port):
    """
    Starts the CryptVault Server on port 8000 by default, after start-up the server
    accepts requests.
    """
    uvicorn.run("cryptvault.main:cryptvault_server", host = host, port = int(port))