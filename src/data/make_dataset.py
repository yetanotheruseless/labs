# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import shutil
import random
import boto3
import tarfile
import io


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")


def create_data_splits(source_dir, dest_dir, train_ratio=0.8, test_ratio=0.1, valid_ratio=0.1):
    assert train_ratio + test_ratio + valid_ratio == 1, "Ratios must sum to 1."

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for split in ['train', 'test', 'validation']:
        split_dir = os.path.join(dest_dir, split)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)

    all_files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]
    random.shuffle(all_files)

    train_files = all_files[:int(len(all_files) * train_ratio)]
    test_files = all_files[int(len(all_files) * train_ratio):int(len(all_files) * (train_ratio + test_ratio))]
    valid_files = all_files[int(len(all_files) * (train_ratio + test_ratio)):]

    for file in train_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, 'train', file))

    for file in test_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, 'test', file))

    for file in valid_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, 'validation', file))


def download_and_uncompress_tgz(aws_key, aws_secret, bucket_name, s3_object_key, local_directory):
    # Initialize a boto3 client with the provided AWS credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )

    # Download the .tgz file from the S3 bucket into memory
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=s3_object_key)
    tgz_data = s3_response['Body'].read()

    # Load the .tgz data into a file-like buffer
    tgz_buffer = io.BytesIO(tgz_data)

    # Uncompress the .tgz file and extract its contents to the specified local directory
    with tarfile.open(fileobj=tgz_buffer, mode="r:gz") as tar:
        tar.extractall(path=local_directory)

    print(f"Downloaded and uncompressed {s3_object_key} from bucket {bucket_name} to {local_directory}")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
