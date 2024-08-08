""" Utility script to read the contents of pdf and convert the llm response to csv file """

import os
import PyPDF2
import json
import traceback


# Read contents of file in .pdf or .txt file format
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        except Exception as e:
            raise Exception("error reading the PDF file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
        )

# Clean the generated reposnse from llm
def extract_json(markdown_string):
    start_marker = '```json'
    end_marker = '```'
    start = markdown_string.find(start_marker) + len(start_marker)
    end = markdown_string.find(end_marker, start)
    return markdown_string[start:end].strip()


# Get table data from cleaned json
def get_table_data(cleaned_json):
    try:
        # Convert the quiz from a str to dict
        quiz_dict = json.loads(cleaned_json)

        quiz_data = []

        # Loop through each question in the data
        for question in data.values():
            mcq = question['mcq']
            options = question['options']
            correct_value = question['correct']
        
            quiz_data.append({
                "MCQ": mcq,
                "CHOICES": options,
                "CORRECT ANSWER": correct_value
            })

        return quiz_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
