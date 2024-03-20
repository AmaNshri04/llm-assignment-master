import datetime
from typing import List, Optional
from http.client import HTTPException
from fastapi import FastAPI, UploadFile , File, Form # Add Form import
from pymongo import MongoClient
from pydantic import BaseModel, conint
from bson.objectid import ObjectId
from gridfs import GridFS
from fastapi.responses import Response, JSONResponse
from bson import ObjectId
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import PyPDF2
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.text_splitter import CharacterTextSplitter 
from langchain_community.vectorstores import FAISS
import io
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with your React app's origin
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


import os
os.environ["OPENAI_API_KEY"]="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"

# Connect to MongoDB
client = MongoClient("mongodb+srv://vipul0592bhatia:yellow*92@cluster0.njkyazj.mongodb.net/")
db = client['project']
fs = GridFS(db)

@app.get("/")
async def root():
    return {"message": "Welcome to your FastAPI application"}


@app.post("/upload_pdf")
async def upload_pdf(background_tasks: BackgroundTasks, question: str = Form(...), file: UploadFile = File(...)): 
    # Read file content
    content = await file.read()  

    # Add the question to the background task data
    background_tasks.add_task(process_pdf_content, content, question)

    # Create a unique filename (optional)
    filename = f"{file.filename}"

    # Store the PDF in GridFS
    pdf_id = fs.put(content, filename=filename)

    # Get Langchain response
    response = await process_pdf_content(content, question)

    # Return JSON response with success message, PDF ID, and Langchain response
    return {"message": "PDF uploaded successfully", "pdf_id": str(pdf_id), "langchain_response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

async def process_pdf_content(file_content: bytes, question: str):
    pdf_file = io.BytesIO(file_content)
    pdfreader = PyPDF2.PdfReader(pdf_file)
    
    raw_text=" "
    for i, page in enumerate(pdfreader.pages):
        content= page.extract_text()
        if content:
            raw_text +=content

    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 800,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings()
    document_search = FAISS.from_texts(texts, embeddings)
   
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = document_search.similarity_search(question)
    response = chain.run(input_documents=docs, question=question)

    return response  # Returning the response instead of printing it
