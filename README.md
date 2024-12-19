# Fipsar GenAI: RAG Search

## Table of Contents

- [Disclaimer](#disclaimer)
- [Dependencies](#dependencies)
- [How to use](#how-to-use) 
- [Methodology](#methodology)

## Disclaimer

This is my first attempt at making a RAG search program and is not representative of production-level code. Additionally, the program is limited by hardware and is required to use smaller scale LLM models (ex. GPT-2), and as such, the results are not ideal for a RAG search program.

## Dependencies

The following libraries are required to run the all aspects of the program:

- pdfplumber
- PyMuPDF
- tabula-py
- faiss-cpu
- numpy
- transformers
- sentence-transformers

## How to use

If you would like to run the program, follow these steps:

```sh
git clone https://github.com/ayydarsh/Fipsar-GenAI
cd Fipsar-GenAI
python extraction.py
```

Next, open the Jupyter notebook `RAG search.ipynb` with an editor of your choice and run each cell in order.

## Methodology

### Introduction

The goal of this project was to create a Retrieval-Augmented Generation (RAG) program which can be queried to produce textual context from 20 research documents. Given the requirements of including documents that contain images with textual context and the small sample size, it was logical to manually acquire the documents. The documents can be found in the `documents` folder. `extraction.py` handles preprocessing the data to structure it in a way to be used by the LLM and for tracking of images and tables associated with a document's text.

### Preprocessing

Extracting text, images, and tables from a PDF is straightforward as there are libraries that are designed to make this process simple. The main idea of the extraction script was for large-scale usability and adaptability. There is a function that processes individual PDF documents and there is a function that passes all the documents in a directory through that function and outputs the result to a specified directory. The second function allows this script to be used for other tasks or projects since it can handle directories.

Halfway through writing this, I remembered that I manually acquired the documents, so I quickly wrote `metadata.json`, which contains each document's title and link. Then I added a function that reads the metadata JSON file and adds the necessary information to the preprocessed results. 

In a production-level project, this whole process would be done through APIs and an automated metadata system, since the project would likely handle much larger volumes of research documents.

### RAG Search

The notebook has step by step explanations, but for an overview, I used a sentence transformer model for the actual RAG search. I chose `all-MiniLM-L6-v2` because it's lightweight and efficient. Then I used GPT-2 for response generation based on a query.

### Results

After experimenting with a few prompts, I came to the conclusion that the model can't fully digest the volume of text since it doesn't have as many parameters (only 124M). This was due to hardware limitations as I wasn't able to run larger models due to lack of computational power and mainly memory constraints. I tried larger models, but they would crash after trying to allocate a large amount of memory that was not available. In a production environment I would assume I have access to cloud computing resources to make use of larger models or API access to models that can process on their platform (ex. OpenAI). 