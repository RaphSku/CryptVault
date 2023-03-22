# CryptVault
Encrypt secrets for use in application code via AES256

## Installation

## Overview over CryptVault
If you run
```bash
cryptvault
```
you should see the following output on your CLI:
<img src="https://github.com/RaphSku/CryptVault/blob/assets/cryptvault_cli_view.png" />
which should list all of the available commands. The most important command is `start` since it will start the CryptVault server. If you use the flag `--help`, you should see the following view
<img src="https://github.com/RaphSku/CryptVault/blob/assets/cryptvault_cli_help_view.png" />
that helps you decide which flags you need to use.

### How to use CryptVault
You can either use directly POST and GET requests in order to communicate with the CryptVault server or you can also use the client interface which is build into the CryptVault library. 

In order to start the server with https enabled, which is highly recommended, you can simply run
```
cryptvault start --host=<host> --port=<port> --sslkeyfile=<path_to_sslkeyfile> --sslcertfile=<path_to_sslcertfile>
```
If you only intend to run CryptVault on your local machine and you don't need https enabled, you can simply run
```
cryptvault start --host=<host> --port=<port>
```
If you run this command without any flags applied, CryptVault will try to start on localhost at port 8000.

#### Case 1: POST & GET requests
You can use POST requests in order to store secrets in the CryptVault. Execute the following curl command in a terminal
```bash
curl --location '<host>:<port>/cryptvault' \
  --header 'Content-Type: application/json' \
  --data '{
    "guid": "<guid>",
    "context": "<context>",
    "secrets": [
        {"key": "<key1>", "value": "<value1>"},
        {"key": "<key2>", "value": "<value2>"}
    ]
  }'
```
in order to store 2 secrets under a context and guid. A guid is used in order to identify you as being the holder of the secrets and a context is applied for grouping.

If you need to get a secret back, just use the following GET request via curl:
```bash
curl --location '<host>:<port>/cryptvault?guid=<guid>&key=<key1>&context=<context>'
```
This guid will be compared with the guid that the registry manages, if those two matches, you get your secret back, otherwise your request will get rejected.
