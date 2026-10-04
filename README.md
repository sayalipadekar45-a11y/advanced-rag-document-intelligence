\# Advanced RAG Document Intelligence System



An advanced \*\*Retrieval-Augmented Generation (RAG)\*\* based document intelligence system that allows users to upload multiple documents and ask questions using semantic search, keyword retrieval, hybrid retrieval, and cross-encoder reranking.



The system is designed to improve document-based question answering by retrieving relevant information from uploaded documents before generating a grounded response.



\---



\## 🚀 Key Features



\- 📄 Upload multiple \*\*PDF, DOCX and TXT\*\* documents

\- ✂️ Intelligent word-based document chunking

\- 🧠 Semantic embeddings using \*\*Sentence Transformers\*\*

\- ⚡ Fast vector similarity search using \*\*FAISS\*\*

\- 🔎 Keyword-based retrieval using \*\*BM25\*\*

\- 🔀 Hybrid retrieval combining semantic and keyword search

\- 🎯 Cross-Encoder based result reranking

\- 💬 Conversational question answering

\- 📚 Multi-document knowledge base

\- 📌 Source and page tracking

\- 🛡️ Basic hallucination control through relevance filtering

\- 🖥️ Professional web interface using Flask, HTML, CSS and JavaScript

\- 🔐 `.env` and uploaded documents protected through `.gitignore`



\---



\## 🏗️ System Architecture



```text

&#x20;                 ┌─────────────────────┐

&#x20;                 │   Upload Documents  │

&#x20;                 │  PDF / DOCX / TXT   │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │   Text Extraction   │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │  Text Cleaning \&    │

&#x20;                 │      Chunking       │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │ Sentence Transformer│

&#x20;                 │     Embeddings      │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │      FAISS          │

&#x20;                 │  Vector Retrieval   │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;             ┌──────────────┴──────────────┐

&#x20;             │                             │

&#x20;             ▼                             ▼

&#x20;      ┌─────────────┐               ┌─────────────┐

&#x20;      │    BM25     │               │   Semantic  │

&#x20;      │   Search    │               │   Search    │

&#x20;      └──────┬──────┘               └──────┬──────┘

&#x20;             │                             │

&#x20;             └──────────────┬──────────────┘

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │  Hybrid Retrieval   │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │  Cross-Encoder      │

&#x20;                 │     Reranking       │

&#x20;                 └──────────┬──────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                 ┌─────────────────────┐

&#x20;                 │ Grounded Response   │

&#x20;                 │ + Source Tracking   │

&#x20;                 └─────────────────────┘

```



\---



\## 🧠 How RAG Works



Traditional language models may generate answers that are not supported by the user's documents.



RAG solves this problem by retrieving relevant information from a knowledge base before producing an answer.



\### Pipeline



```text

Document

&#x20;  ↓

Chunking

&#x20;  ↓

Embeddings

&#x20;  ↓

Vector Database

&#x20;  ↓

Retrieval

&#x20;  ↓

Reranking

&#x20;  ↓

Relevant Context

&#x20;  ↓

Grounded Answer

```



The system retrieves relevant document chunks instead of relying only on previously learned model knowledge.



\---



\## 🔍 Retrieval Strategy



This project uses a \*\*hybrid retrieval architecture\*\*.



\### 1. Semantic Retrieval



Sentence Transformers convert document chunks into numerical vectors called embeddings.



FAISS then performs similarity search between the user's question and document embeddings.



This helps identify documents with similar meaning even when the exact keywords are different.



\### 2. BM25 Keyword Retrieval



BM25 performs keyword-based information retrieval.



It is useful when exact terms, technical words, names or identifiers are important.



\### 3. Hybrid Retrieval



The project combines:



```text

Semantic Search

&#x20;     +

BM25 Keyword Search

&#x20;     ↓

Hybrid Retrieval

```



This provides a stronger retrieval strategy than relying on only one method.



\### 4. Cross-Encoder Reranking



The retrieved candidates are passed to a Cross-Encoder.



The Cross-Encoder evaluates the relationship between:



```text

Question + Document Chunk

```



and reranks the candidates according to relevance.



\---



\## 🛠️ Technologies Used



| Technology | Purpose |

|---|---|

| Python | Backend development |

| Flask | Web application framework |

| Sentence Transformers | Text embeddings |

| FAISS | Vector similarity search |

| BM25 | Keyword retrieval |

| Cross-Encoder | Reranking |

| PyMuPDF | PDF text extraction |

| python-docx | DOCX processing |

| HTML | Frontend structure |

| CSS | UI design |

| JavaScript | Frontend interaction |

| python-dotenv | Environment configuration |



\---



\## 📁 Project Structure



```text

advanced-rag-document-intelligence/

│

├── app.py

├── requirements.txt

├── .env.example

├── .gitignore

├── README.md

│

├── rag/

│   ├── \_\_init\_\_.py

│   ├── document\_loader.py

│   ├── chunker.py

│   ├── embeddings.py

│   ├── vector\_store.py

│   ├── bm25\_retriever.py

│   ├── hybrid\_retriever.py

│   ├── reranker.py

│   ├── generator.py

│   └── pipeline.py

│

├── templates/

│   └── index.html

│

└── static/

&#x20;   ├── style.css

&#x20;   └── script.js

```



\---





\## 📄 Supported Documents



The system currently supports:



\- PDF

\- DOCX

\- TXT



Multiple documents can be uploaded together to create a combined searchable knowledge base.



\---



\## 💬 Example Questions



After uploading documents, users can ask questions such as:



```text

What is this document about?



Explain the main concept discussed in the document.



What are the important points?



Which device is responsible for connecting different networks?



What is the difference between LAN and WAN?

```



The system retrieves relevant document chunks and displays source information including:



\- Document

\- Page

\- Chunk ID

\- Relevance score



\---



\## 🛡️ Hallucination Control



The system includes a basic relevance-based filtering mechanism.



If the retrieved content is not sufficiently relevant, the system avoids presenting unrelated document content as an answer.



This provides a basic safeguard against unsupported responses.



> Note: The current implementation uses a local grounded answer generator rather than an external generative LLM API. The architecture can be extended with an LLM provider for natural-language answer generation.



\---



\---



\## 📊 Advantages



\- Supports multiple document formats

\- Supports multiple documents

\- Combines semantic and keyword retrieval

\- Uses reranking for improved relevance

\- Provides document source tracking

\- Reduces dependence on keyword-only search

\- Provides a practical document intelligence interface

\- Modular architecture allows future improvements



\---



\## 🔮 Future Improvements



Possible future extensions include:



\- Integration with local LLMs such as Ollama

\- Integration with OpenAI or other LLM APIs

\- Persistent vector database

\- Advanced query rewriting

\- Better conversational memory

\- Retrieval evaluation metrics

\- OCR support for scanned documents

\- Metadata filtering

\- Authentication and user accounts

\- Streaming responses

\- Cloud deployment

\- Advanced citation generation



\---



\## 🎯 Project Objective



The objective of this project is to demonstrate how modern \*\*Retrieval-Augmented Generation systems\*\* can combine:



```text

Document Processing

&#x20;       +

Embeddings

&#x20;       +

Vector Search

&#x20;       +

Keyword Search

&#x20;       +

Hybrid Retrieval

&#x20;       +

Reranking

&#x20;       +

Grounded Answering

```



to build an intelligent document question-answering system.



\---

sayali padekar

Computer Engineering Student



GitHub:  

https://github.com/sayalipadekar45-a11y



LinkedIn:  

https://linkedin.com/in/sayali-padekar-a9a859430

