from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_docs(path="data/"):
    loader = DirectoryLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)
    print(f"Loaded and split {len(chunks)} chunks from documents in {path}")
    return chunks
#chunks_created=load_and_split_docs()
#print(f"Total chunks created: {len(chunks_created)}, Sample chunk: {chunks_created[0]}")