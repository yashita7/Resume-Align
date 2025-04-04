from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

##Streamlit
st.set_page_config(page_title="ATS Resume expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume in pdf format : ",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the Resume")

# submit2 = st.button("How can I improvise my skills ?")

submit2 = st.button("Percentage Match ")

input_prompt1 = """
 You are an experienced Technical HR with tech experience in the field of any one job role from data Science or full stack web development or 
 big data engineering or DEVOPS or Data Analyst, your task is to review the provided resume against the job description for these profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS(application tracking System) scanner with a depp understanding in the field of any one job role from of data Science or
 full stack web development or big data engineering or DEVOPS or Data Analyst and deep ATS functionality.
 Your task is to evaluate the resume against the provided job description. First the output should come as percentage and then
 keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload the resume")
    
elif submit2 :
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload the resume")
