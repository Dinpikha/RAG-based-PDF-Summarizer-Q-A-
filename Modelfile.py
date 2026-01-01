import streamlit as st
from pypdf import PdfReader
import re
from chromadb.config import Settings
import numpy as np
import chromadb
import os 
from docling.document_converter import DocumentConverter
convt=DocumentConverter()
from ollama import chat
from ollama import ChatResponse
client_chroma=chromadb.Client(    settings=Settings(
    is_persistent=True,
        persist_directory="chromastore"
    ))
collection=client_chroma.get_collection('Rag')
st.title('My pdf Summarizer! ')

import streamlit as st
import os
pdf_folder='pdfs'
pdf_files=[f for f in os.listdir(pdf_folder) if f.endswith('.pdf') ]
selected_pdf = st.selectbox("Data", pdf_files)

st.markdown("""
<style>
.file-card {
    background: #eff6ff;
    padding: 16px;
    border: 2px solid #3b82f6;
    border-radius: 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 10px rgba(59,130,246,0.15);
    transition: all 0.2s ease-in-out;
}

.file-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(59,130,246,0.25);
}

.file-name {
    font-size: 16px;
    font-weight: 600;
    color: #1e3a8a;
}
</style>
""", unsafe_allow_html=True)

if selected_pdf :
    st.markdown(f"{selected_pdf}")

    with st.container():

        with open(os.path.join(pdf_folder, selected_pdf), "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=selected_pdf,
                key="download_btn",
                use_container_width=True  
            )




    opwuestion=st.text_input('Enter a Question')
    btndone=st.button('Generate Response')
    

if btndone and opwuestion :
    
        with st.spinner("Processing... please wait "):
            results=collection.query(
                query_texts=[opwuestion],
                n_results=3

            )
            context= "\n\n".join(results["documents"][0])
            theselectedtext=context
            # st.write(theselectedtext)
            # prompt = f"""
            # instructions = "You are a Helpful Question answer Assistant .You have to understand what the words mean from the chunks provided and respond to the user using ONLY the chunks. If the answer is not in the chunks, reply exactly: 'I do not have enough data to answer.'"
            # chunks = "{theselectedtext}"
            # question = "{opwuestion}"
            # """

        response: ChatResponse = chat(
    model='llama3.2:3b',
    messages=[
        {
            "role": "system",
            "content": (
                "You are a retrieval-based QA system.\n"
                "You MUST ONLY answer using the provided document text.\n"
                "If the answer is not explicitly stated in the document text, "
                "Say:\n"
                "I do not have enough data to answer."
            )
        },
        {
            "role": "user",
            "content": f"""
DOCUMENT TEXT:
{theselectedtext}

QUESTION:
{opwuestion}

Find the answer in the document and explain it clearly.
If you cannot find it, say:
I do not have enough data to answer.
"""

        }
    ]
)

        answer=response.message.content

            

        st.write(answer)
        
