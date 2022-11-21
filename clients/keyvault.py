from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential



class KeyvaultClient:


    def __init__(self, keyvault_name: str, credential = DefaultAzureCredential()):

        print(f"Connecting to keyvault '{keyvault_name}'")
        self._url = f"https://{keyvault_name}.vault.azure.net"
        self._credential = credential
        self._client = SecretClient(vault_url=self._url, credential=self._credential)

    def get_secret(self, secret_name: str) -> str:

        print(f"Getting secret with name '{secret_name}'")
        return self._client.get_secret(secret_name).value

    def set_secret(self, secret_name: str, secret_value: str):

        print(f"Setting secret with name '{secret_name}'")
        self._client.set_secret(secret_name, secret_value)

    def delete_secret(self, secret_name: str):

        print(f"Deleting secret '{secret_name}'")
        self._client.begin_delete_secret(secret_name)