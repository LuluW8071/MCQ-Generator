import json
import traceback
import pandas as pd
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.utils import read_file, extract_json, get_table_data
from src.mcq_generator.generate_mcq import generate_evaluate_chain


# Load JSON Response format file
with open("./response.json", "r") as file:
    RESPONSE_JSON = json.load(file)


# Set page configuration
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("MCQ Generator")
st.write("Generate multiple-choice questions (MCQs) from a text or pdf file.")

# Sidebar
with st.sidebar:
    st.subheader("Input Parameters")
    file_upload = st.file_uploader(
        "Upload file in .txt or .pdf format", type=["txt", "pdf"])
    mcq_count = st.number_input(
        "Count of MCQs", min_value=3, max_value=10, value=5, step=1)
    topic = st.text_input("Topics or Subject to generate MCQ",
                          max_chars=25, placeholder="e.g., Mathematics")
    difficulty = st.text_input(
        "Difficulty Level", max_chars=20, placeholder="e.g., simple, mid, hard, very hard")
    generate_button = st.button("Generate MCQs")


# Main content
if file_upload and generate_button:
    with st.spinner("Generating MCQs..."):
        try:
            # Read the file
            text = read_file(file_upload)

            # Generate MCQs
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": topic,
                    "tone": difficulty,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
            )

            if isinstance(response, dict):
                quiz = response.get("quiz")
                if quiz is not None:
                    cleaned_json = extract_json(quiz)
                    # print(cleaned_json)
                    table_data = get_table_data(cleaned_json)
                    # print(table_data)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        # print(df)
                        df.index = df.index + 1
                        st.subheader("Generated MCQs")
                        st.table(df)

                        # Display the table in a review box
                        # st.subheader("Review")
                        # st.text_area(
                        #     label="", value=response["review"], height=200)

                        # Download the table
                        st.download_button(
                            label="Download as CSV",
                            data=df.to_csv(index=False),
                            file_name="mcq.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error("Error in table data")
                else:
                    st.error("Error in generating MCQ")

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An error occurred while generating MCQs.")
