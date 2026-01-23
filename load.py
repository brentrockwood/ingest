import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# 1. INGEST: Load all markdown files from a directory
loader = DirectoryLoader("../network-docs/", glob="**/*.md", loader_cls=TextLoader)
docs = loader.load()

# 2. CHUNK: Split documents specifically for Markdown structure
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
chunked_docs = text_splitter.split_documents(docs)

# 3. EMBED & STORE: Send to your local Docker Qdrant instance
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Connect to your local Docker Qdrant container
qdrant_url = os.getenv("QDRANT_API")
collection_name = "network_docs"

vector_store = QdrantVectorStore.from_documents(
    chunked_docs,
    embeddings,
    url=qdrant_url,
    collection_name=collection_name,
)

print(f"Successfully loaded {len(chunked_docs)} chunks into Qdrant collection: {collection_name}")

