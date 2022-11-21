from clients.keyvault import KeyvaultClient
from azure.identity import DefaultAzureCredential

keyvault_name = "sebastian-test-vault"
kv_client = KeyvaultClient(keyvault_name, credential=DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_visual_studio_code_credential=True,
    exclude_shared_token_cache_credential=True
))

db_server   = kv_client.get_secret("db-server")
db_username = kv_client.get_secret("db-username")
db_password = kv_client.get_secret("db-password")
db_name = kv_client.get_secret("db-name")

schema = "sebastian_test"


