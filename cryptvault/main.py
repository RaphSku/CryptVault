import click
import uvicorn
import sys
import os
import pkg_resources

from fastapi import FastAPI

sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
import cryptvault.routes.get  as get
import cryptvault.routes.post as post

from cryptvault.group    import CustomGroup
from cryptvault.commands import VersionCommand, StartCommand, GenerateCommand


cryptvault_server = FastAPI()

cryptvault_server.include_router(get.get_router)
cryptvault_server.include_router(post.post_router)


@click.group(cls = CustomGroup)
def main():
    """
    CryptVault is a vault which encrypts your secrets and
    stores them for you 
    """
    pass


@main.command(cls = StartCommand)
@click.option('--host', '-h', default = "localhost", help = 'host on which the server should run')
@click.option('--port', '-p', default = "8000", help = 'port assigned to the server')
@click.option('--sslkeyfile', default = "", help = 'ssl keyfile for enabling https')
@click.option('--sslcertfile', default = "", help = 'ssl certificate file for enabling https')
def start(host, port, sslkeyfile, sslcertfile):
    """
    Starts the CryptVault Server on port 8000 by default, after start-up the server
    accepts requests.
    """
    if host != "localhost" or host != "127.0.0.1":
        uvicorn.run("cryptvault.main:cryptvault_server", 
                    host = host, 
                    port = int(port), 
                    ssl_keyfile = sslkeyfile, 
                    ssl_certfile = sslcertfile)    
    uvicorn.run("cryptvault.main:cryptvault_server", host = host, port = int(port))


@main.command(cls = VersionCommand)
def version():
    """
    Prints the current version of the cryptvault library
    """
    print(f"CryptVault version: {pkg_resources.get_distribution('cryptvault').version}")


@main.command(cls = GenerateCommand)
def generate():
    """
    Generates JSON body template for the post request
    """
    print("""
    {
        "guid": "<guid>",
        "context": "<context>",
        "secrets": [
            {"key": "<key>", "value": "<value>"},
            {"key": "<key2>", "value": "<value2>"}
        ]
    }""")
