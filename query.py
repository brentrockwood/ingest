import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def query_qdrant(question):
    # 1. Setup the same embedding model used during ingestion
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 2. Connect to the existing Qdrant collection
    url = os.getenv("QDRANT_API")
    collection_name = "network_docs"
    
    client = QdrantClient(url=url)
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name=collection_name, 
        embedding=embeddings
    )

    # 3. Perform the search
    # k=3 retrieves the top 3 most relevant matches
    results = vector_store.similarity_search(question, k=3)

    # 4. Print results
    print(f"\n--- Results for: '{question}' ---\n")
    for i, doc in enumerate(results):
        source = doc.metadata.get('source', 'Unknown')
        print(f"Result {i+1} (Source: {source}):")
        print(f"{doc.page_content}\n")
        print("-" * 30)

if __name__ == "__main__":
    # Check if a query was provided as a CLI argument
    if len(sys.argv) < 2:
        print("Usage: python3 query.py 'your question here'")
    else:
        user_query = " ".join(sys.argv[1:])
        query_qdrant(user_query)

