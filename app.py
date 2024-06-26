import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2 as pdf

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_respnse(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_resume(file):
    text=''
    reader = pdf.PdfReader(file)

    for page in range(len(reader.pages)):
        content = reader.pages[page]
        text += str(content.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

#Streamlit App
st.set_page_config('Improve your Resume Demo')
st.title('ATS AI assistant')
st.text("Improve Your Resume ATS")
jd = st.text_input('Enter your jd here')
upload_file = st.file_uploader('Upload your resume here:', type='pdf', help='Please upload pdf only')

submit = st.button('Submit')

if submit:
    if upload_file is not None:
        text = input_resume(upload_file)
        response = get_gemini_respnse(input_prompt)
        st.subheader('Your Analysis: ')
        st.write(response)


