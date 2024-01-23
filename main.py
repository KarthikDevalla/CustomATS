import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as ai
import os 

st.title('Applicant Tracking System')

load_dotenv()

ai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def text_from_pdf(filename):
    pdf=PdfReader(filename)
    text=''
    for page in range(len(pdf.pages)):
        page=pdf.pages[page]
        text+=str(page.extract_text())
    return text

def get_answer(prompt):
    model = ai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

custom_prompt="""
You are a very skilled and professional ATS (Applicant Tracking System) with a deep understanding of the tech field, software engineering, data sceince, machine learning engineer.
Your task to evalute this resume based on the given job description. You must consider the current job market is very competitive and should 
provide best assistance for improving the resumes. Assign the matching percentage based on job description and missing keywords with very high accuracy. 
resume:{text}
job desciption: {job_description}
Answer it in the following manner {'Matching Percent':'%','Missing Keywords:[]','Summary':''}
"""

job_description=st.text_area('Job Description')
uploaded_resume=st.file_uploader('Upload your Resume')
results=st.button('Get Results')
if results:
    if uploaded_resume is not None:
        text_from_pdf(uploaded_resume)
        answer=get_answer(custom_prompt)
        st.write(answer)





