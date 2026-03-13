from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

def create_vector_store(docs):
    embeddings = OpenAIEmbeddings()

    client = QdrantClient(":memory:")  # local mode

    vectorstore = QdrantVectorStore.from_documents(
        docs,
        embeddings,
        client=client,
        collection_name="ocs_docs"
    )

    return vectorstore