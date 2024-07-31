## IMPORTS

import os
import pdfplumber
from docx import Document
import requests
import json


## METHODS 

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
    
def extract_requirements(text):
    prompt = text + "Your task is to retrieve all the requirements from this text. You should absolutely present it like this: 1.[Requirement ID] : [Requirement description] \n 2.[Requirement ID] : [Requirement description] \n 3.[Requirement ID] : [Requirement description] \n, etc. Make sure to be exhaustive, we cannot afford to let a single requirement unreported."
    url = 'https://obxy6jphzf.execute-api.eu-west-1.amazonaws.com/dev/question'  
    payload = {
        'body': {
            'request': prompt
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print("Response: ", response)

    if response.status_code == 200:
        response_payload = response.json()
        body = json.loads(response_payload['body'])
        print("body: ", body)
        generated_text = body['model_response']
        print("generated_text: ", generated_text)
        requirements = generated_text.split('\n')  # Assuming each requirement is separated by a newline
        print("requirements: ", requirements)
        return [req.strip() for req in requirements[1:] if req.strip()]
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")


def save_requirements(requirements, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, req in enumerate(requirements):
        with open(os.path.join(output_dir, f"requirement_{i+1}.txt"), "w", encoding="utf-8") as file:
            file.write(req)
            

## MAIN

def main(file_path, output_dir):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_word(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")
    print("Text extracted")
    requirements = extract_requirements(text)
    print("Requirements extracted")
    save_requirements(requirements, output_dir)
    print("Requirements saved")



# Example usage
file_path = "C:/PythonProjects/RequirementSplitting/Simplified_SRS_with_Sections.pdf"  
output_dir = "C:/PythonProjects/RequirementSplitting/output_requirements"

main(file_path, output_dir)
