from typing import NamedTuple

from google.cloud import secretmanager


def get_secret(secret_name, proj='aigamer-382421'):
#    auth.authenticate_user()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": f"projects/{proj}/secrets/{secret_name}/versions/latest"})
    return response.payload.data.decode('UTF-8')


def get_aws_creds():
    aws_key = get_secret('aws-key')
    aws_secret = get_secret('aws-secret')
    return aws_key, aws_secret


def get_github_creds(out_path='github-key'):
    key_str = get_secret('github-key')
    with open(out_path, 'w') as f:
        f.write(key_str)


Keys = NamedTuple('keys', [('aws_key', str), ('aws_secret', str), ('pinecone_api_key', str), ('openai_api_key', str)])


def get_keys() -> Keys:
    aws_key, aws_secret = get_aws_creds()
    pinecone_api_key = get_secret('pinecone-api-key')
    openai_api_key = get_secret('openai-api-key')
    return Keys(aws_key, aws_secret, pinecone_api_key, openai_api_key)

