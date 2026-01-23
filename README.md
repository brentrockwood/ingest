# Network Documentation Ingestion System

This project provides a Python-based system for ingesting network documentation into a vector database (Qdrant) and querying it using semantic search. It leverages OpenAI's embeddings and LangChain to process Markdown documents and enable intelligent querying of network infrastructure documentation.

## Overview

The system consists of two main scripts:
- **`load.py`** - Ingests Markdown documents into a Qdrant vector store
- **`query.py`** - Allows semantic querying of the ingested documentation

## Dependencies

### Python Packages
Install the required packages using the provided requirements file:

```bash
pip install -r requirements.txt
```

The following packages are required:
- `langchain` - Core framework for document processing
- `langchain-community` - Community extensions
- `langchain-openai` - OpenAI integration
- `langchain-qdrant` - Qdrant vector store integration
- `langchain-text-splitters` - Document splitting utilities

### Environment Variables

Before running the scripts, set the following environment variables:

```bash
# Required: OpenAI API key for embeddings
export OPENAI_API_KEY="your-openai-api-key-here"

# Required: Qdrant database URL
export QDRANT_API="http://your-qdrant-host:6333"
```

### External Dependencies

1. **Qdrant Vector Database**: A running Qdrant instance is required. The system expects Qdrant to be accessible at the URL specified by the `QDRANT_API` environment variable.

2. **Network Documentation**: The `load.py` script expects Markdown files to be located in `../network-docs/` relative to the project directory.

## Usage

### Ingesting Documents

To load and index network documentation:

```bash
python load.py
```

This script will:
1. Load all Markdown files from `../network-docs/`
2. Split documents into chunks optimized for Markdown structure (1000 characters with 100-character overlap)
3. Generate embeddings using OpenAI's `text-embedding-3-small` model
4. Store the chunks in a Qdrant collection named `network_docs`

### Querying the Documentation

To search the ingested documentation:

```bash
python query.py "your question here"
```

Example queries:
```bash
python query.py "What kind of router do I have?"
python query.py "How is the firewall configured?"
python query.py "What are the VPN settings?"
```

The query script will:
1. Use the same embedding model as the ingestion process
2. Search the Qdrant collection for the most relevant documents
3. Return the top 3 most similar chunks with their source files

## Architecture

### Document Processing Pipeline

1. **Load**: Uses `DirectoryLoader` to read all Markdown files
2. **Chunk**: Employs `MarkdownTextSplitter` for context-aware splitting
3. **Embed**: Generates vector embeddings using OpenAI's text-embedding model
4. **Store**: Persists vectors in Qdrant for efficient similarity search

### Semantic Search

The system uses vector similarity search to find documentation chunks that are semantically related to the query, allowing for more intelligent search compared to simple keyword matching.

## Configuration

- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 100 characters
- **Embedding Model**: `text-embedding-3-small`
- **Collection Name**: `network_docs`
- **Search Results**: Returns top 3 matches by default

## Security Considerations

- All sensitive information (API keys, database URLs) is externalized to environment variables
- No hardcoded credentials in the source code
- Ensure the `.ai/config.json` file (if present) does not contain sensitive information

## Directory Structure

```
ingest/
├── load.py              # Document ingestion script
├── query.py             # Query script for semantic search
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── ../network-docs/    # Source Markdown documents (outside project)
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure Qdrant is running and accessible at the URL specified by `QDRANT_API`
2. **Authentication Errors**: Verify that `OPENAI_API_KEY` is set and valid
3. **Document Not Found**: Ensure the `../network-docs/` directory exists and contains Markdown files
4. **Collection Already Exists**: The script will reuse existing collections; delete the collection in Qdrant if you need to reindex from scratch

### Debugging

- Set environment variables before running the scripts
- Check Qdrant logs for connection issues
- Verify document paths and file permissions
- Monitor OpenAI API usage if encountering rate limits

## License

This project is provided as-is for internal network documentation management.