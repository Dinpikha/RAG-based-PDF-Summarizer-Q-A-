This project is a PDF Summarizer 


Pipeline:
Import the PDfs -> Docling -> ChromaDB -> Streamlit UI -> Ollama (llama3.2:3b) ->  Output 

## Demo

<img src="images/food_at_the_hotel.jpeg" width="600">

<img src="images/model_summarizes_the_protein_cheat_sheet.jpeg" width="600">

Libraries & Tools:

Streamlit (UI)
Docling (PDF parsing)
ChromaDB (Vector database)
LangChain (RAG pipeline)
Ollama (Local LLM)
Sentence Transformers (Embeddings)

Run LLM:

ollama run llama3.2:3b

Highlights:
Hallucination prevention via context grounding
Fully local LLM (no external API dependency)
