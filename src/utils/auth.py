from google.cloud import secretmanager
from google.colab import auth


def get_secret(secret_name, proj='aigamer-382421'):
    auth.authenticate_user()
    client = secretmanager.SecretManagerServiceClient()
    return client.access_secret_version(request={"name": f"projects/{proj}/secrets/{secret_name}/versions/latest"})


def get_aws_creds():
    aws_key = get_secret('aws-key').payload.data.decode('UTF-8')
    aws_secret = get_secret('aws-secret').payload.data.decode('UTF-8')
    return aws_key, aws_secret


def get_github_creds():
    key_str = get_secret('github-key')
    