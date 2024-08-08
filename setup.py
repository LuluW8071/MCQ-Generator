from setuptools import find_packages, setup

setup(
    name="MCQ-Generator",
    version="0.0.1",
    author="Shashin Maharjan",
    author_email="shashinmaharjan@example.com",
    description="A simple multiple-choice question generator for educational purposes",
    url="https://github.com/luluw/MCQ-Generator",
    packages=find_packages(),
    install_requires=["langchain", "langchain-community", "langchain-google-genai",
                      "streamlit", "ipykernel", "python-dotenv", "ipywidgets", "PyPDF2"]
)
