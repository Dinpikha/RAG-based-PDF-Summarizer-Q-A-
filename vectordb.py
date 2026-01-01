import chromadb
import os 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.config import Settings
client = chromadb.Client(
    settings=Settings(
        is_persistent=True,
        persist_directory="chromastore"
    )
)
collection = client.create_collection(name="Rag")
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
)


for filename in os.listdir('md-folder'):
    if not filename.endswith('.md'):
        continue
    path=os.path.join('md-folder',filename)
    with open(path,'r',encoding='utf-8')as f:
        data=f.read()
    chunks=text_splitter.split_text(data)

    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
results=collection.query(
    query_texts='What is the 80 percent rule for good health?',
    n_results=1
)
print(results)