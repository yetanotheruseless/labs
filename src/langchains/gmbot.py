from langchain.embeddings.openai import OpenAIEmbeddings, Embeddings
from langchain.vectorstores import Pinecone, VectorStore
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders import S3DirectoryLoader, DirectoryLoader
from .loaders import S3FilesInDirectoryLoader


def get_s3_loader(bucket_name, prefix) -> BaseLoader:
    return S3FilesInDirectoryLoader(bucket=bucket_name, prefix=prefix)


def get_dir_loader(dir_path) -> BaseLoader:
    return DirectoryLoader(path=dir_path)


def get_text_splitter(chunk_size=1000, chunk_overlap=20) -> TextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def get_embeddings(openai_api_key, model="text-embedding-ada-002") -> Embeddings:
    return OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model=model
    )


def get_vectordb(embeddings: Embeddings,
                 pinecone_api_key: str, pinecone_env: str, pinecone_index_name: str) -> VectorStore:
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    # note that this will fail later (when adding documents) if the index doesn't exist
    vector_store: VectorStore = Pinecone.from_existing_index(index_name=pinecone_index_name, embedding=embeddings)
    return vector_store


def index_docs(loader: BaseLoader, splitter: TextSplitter, embeddings: Embeddings, vectordb: VectorStore):
    documents = loader.load()
    texts = splitter.split_documents(documents)
    vectordb.add_documents(documents=texts, embeddings=embeddings)
    return vectordb


def create_qa_chain(openai_api_key, pinecone_api_key, pinecone_env, pinecone_index_name,
                    llm_model_name='gpt-3.5-turbo', embedding_model_name='text-embedding-ada-002',
                    data_uri=None, num_retrieved_docs=5):
    '''
    Create a QA chain with a Pinecone vector store and OpenAI LLM, populated with documents from S3 (if supplied),
    otherwise the pinecone index is assumed to be populated already
    :param data_uri:
    :param num_retrieved_docs:
    :param openai_api_key:
    :param pinecone_api_key:
    :param pinecone_env:
    :param pinecone_index_name:
    :param llm_model_name:
    :param embedding_model_name:
    :param bucket_name:
    :param prefix:
    :return:
    '''

    embeddings = get_embeddings(openai_api_key, model=embedding_model_name)
    vectordb = get_vectordb(embeddings=embeddings, pinecone_api_key=pinecone_api_key, pinecone_env=pinecone_env,
                            pinecone_index_name=pinecone_index_name)
    if data_uri:
        if data_uri.startswith("s3://"):
            bucket_name, prefix = data_uri.split("s3://")[1].split("/", 1)
            loader = get_s3_loader(bucket_name=bucket_name, prefix=prefix)
        elif data_uri.startswith("file://"):
            loader = get_dir_loader(dir_path=data_uri.split("file://")[1])
        else:
            raise ValueError(f"Unsupported data_uri: {data_uri}")
        splitter = get_text_splitter()
        vectordb = index_docs(loader=loader, splitter=splitter, embeddings=embeddings, vectordb=vectordb)
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key, model_name=llm_model_name),
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_type="similarity", search_kwargs={"k": num_retrieved_docs}),
        verbose=True
    )
    return qa


#
# >>> from utils.auth import *
# >>> from langchains.gmbot import *
# >>> keys = get_keys()
# >>> qa = create_qa_chain(openai_api_key=keys.openai_api_key, pinecone_api_key=keys.pinecone_api_key, pinecone_env='us-east4-gcp', pinecone_index_name='game-tmp', llm_model_name='text-davinci-003', data_uri='s3://yetanotheruseless-data/projects/AI-RPG/interim/clean_text/footnotes/')
#
