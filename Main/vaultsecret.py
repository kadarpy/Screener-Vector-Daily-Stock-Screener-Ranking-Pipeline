import hvac 

VAULT_ADDR = "http://127.0.0.1:8200"
VAULT_TOKEN = input("Enter the Vault token : ")
SECRET_PATH = "secret/data/postgres_UP"

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

if client.is_authenticated():
    print("Vault authentication successful!")
else:
    raise Exception("Vault authentication failed!")


secret_response = client.secrets.kv.v2.read_secret_version(path="postgres_UP", mount_point="secret")

creds = secret_response["data"]["data"]
username = creds.get("username")
password = creds.get("password")
host = creds.get("host")

print(f"Retrieved secrets from Vault successfully! \n{username}\n{password}\n{host}")