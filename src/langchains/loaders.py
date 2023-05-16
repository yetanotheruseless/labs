"""Loading logic for loading documents from an s3 directory."""
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.s3_file import S3FileLoader


class S3FilesInDirectoryLoader(BaseLoader):
    """Loading logic for loading documents from s3."""

    def __init__(self, bucket: str, prefix: str = ""):
        """Initialize with bucket and key name."""
        self.bucket = bucket
        self.prefix = prefix

    def load(self) -> List[Document]:
        """Load documents."""
        print("in s3filesindirectoryloader", flush=True)
        try:
            import boto3
        except ImportError:
            raise ValueError(
                "Could not import boto3 python package. "
                "Please install it with `pip install boto3`."
            )
        try:
            import nltk
            import ssl
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

            nltk.download("punkt")
            nltk.download("averaged_perceptron_tagger")
        except ImportError:
            raise ValueError(
                "Could not import nltk python package. "
                "Please install it with `pip install nltk`."
            )
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket)
        docs = []
        for obj in bucket.objects.filter(Prefix=self.prefix):
            if obj.key.endswith("/"):
                print("Skipping directory: ", obj.key, flush=True)
                continue
            print("Loading file: ", obj.key, flush=True )
            loader = S3FileLoader(self.bucket, obj.key)
            docs.extend(loader.load())
        return docs
