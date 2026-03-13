from ingest.splitchunks import load_and_split_docs
from vecstore.storedb import create_vector_store
from retrieve.retrievedata import get_retriever
from generator.generatetc import create_generator
from exporter.exporttoexcel import export_to_excel
from dotenv import load_dotenv

load_dotenv()


def run_pipeline(query: str):
    print("Loading documents...")
    docs = load_and_split_docs()

    print(f"Loaded {len(docs)} chunks")

    vectorstore = create_vector_store(docs)
    retriever = get_retriever(vectorstore)
    generator = create_generator(retriever)

    print("Generating test cases...")
    result = generator(query)

    print("Exporting to Excel...")
    excel_file = export_to_excel(result)  # should return file path

    return result, excel_file


def main():
    query = (
        "Act as expert QA OCS test engineer and generate "
        "OCS test cases based on the requirements and details "
        "provided in the documents."
    )

    result, excel_file = run_pipeline(query)

    print(result)
    print("Excel created:", excel_file)


if __name__ == "__main__":
    main()
