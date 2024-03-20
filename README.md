This project consists of a FastAPI backend and a React frontend. The FastAPI application provides an API for uploading PDF files and submitting questions related to the content of the PDF. 
The uploaded PDF is processed, and a relevant response is generated based on the question asked, utilizing LangChain and OpenAI for processing and extracting information. 

The React application is a simple UI that allows users to upload a PDF file and enter a question to get insights based on the PDF's content.

FastAPI Application
Features

Upload PDF files for processing.
Submit questions related to the content of the uploaded PDF.
Utilizes LangChain and OpenAI to analyze the PDF and generate relevant responses.
Stores uploaded PDF files using MongoDB's GridFS.
Setup and Running
Environment Variables: Set the OPENAI_API_KEY with your OpenAI API key.

MongoDB Connection: Ensure MongoDB is running and accessible. Update the connection string in the code if necessary.

Running the Application: Execute the following command to run the FastAPI application:

bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
Accessing the API: The API can be accessed at http://localhost:8000.

Endpoints
GET /: Returns a welcome message.
POST /upload_pdf: Accepts a PDF file and a question, processes the PDF, and returns a response based on the question.
React Application
Features
User-friendly interface to upload PDF files.
Field to enter questions related to the uploaded PDF.
Displays responses based on the question and the content of the uploaded PDF.
Setup and Running

Installation: Navigate to the project directory and run npm install to install the required dependencies.
Running the Application: Execute npm start to start the React application.
Using the Application: The application will be available at http://localhost:3000. Users can upload a PDF and enter a question to get a response based on the PDF's content.

Interaction Flow

User uploads a PDF file using the file input.
User enters a question related to the content of the uploaded PDF in the provided input field.
User clicks the "Submit" button to send the PDF and the question to the FastAPI backend.
The response from the backend is displayed under the "Result" section.
Note
Ensure both the FastAPI backend and the React frontend are running simultaneously for the system to function correctly. The React application communicates with the FastAPI backend to upload PDFs and receive responses.