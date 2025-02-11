from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import google.generativeai as genai
import pdf2image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
def gemini_response(task,pdf_content,prompt):
    response_model=genai.GenerativeModel('gemini-1.5-pro')
    response=response_model.generate_content([task, pdf_content[0],prompt])
    return response.text

#converting pdf to image
def pdf_conversion(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

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
        raise FileNotFoundError("File not uploaded")
    

## Streamlit app 

st.set_page_config(page_title="ATS TRACKER SYSTEM")
st.header("ATS  Resume tracker")
#Taking job description as input and uploading pdf
input_text=st.text_area("Job Description: ",key=input)
uploaded_file=st.file_uploader("Upload your resume here in pdf  format only",type=["pdf"])


if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' Great!!! Uploaded successfully!")
    st.write("You can now proceed with further processing.")

option1=st.button("Tell me about the resume")
option2=st.button("Percentage(%) match")
option3=st.button("Tell me the skills I need to learn and focus")
## input promts for each option
input_promt_1="""
    you are an expert HR with experience in the field of data science, web development,full stack development, big data analysis, data engineering ,data mining. your is task to analyse and review the resume provided against the job description for these profiles please share your evaluation professionally whether the candidate's profile matches with the job description and highlights given in the chop description and is applicable for the specified job.
 """

input_promt_2="""
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science,data science, web development,full stack development, big data analysis, data engineering ,data mining and ATS functionality, your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
input_promt_3=""" 
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science,data science, web development,full stack development, big data analysis, data engineering ,data mining and ATS functionality, your task is to evaluate the resume against the provided job description. give me the  list of skills requied to learn for a better fit for the job. give the the list of skills in bullet formats only(short and precise)
    """

if option1:
    if uploaded_file is not None:
        pdf_content=pdf_conversion(uploaded_file)
        response=gemini_response(input_promt_1,pdf_content,input_text)
        st.subheader("Here is what I can say about your resume")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif option2:
    if uploaded_file is not None:
        pdf_content=pdf_conversion(uploaded_file)
        response=gemini_response(input_promt_2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif option3:
    if uploaded_file is not None:
        pdf_content=pdf_conversion(uploaded_file)
        response=gemini_response(input_promt_3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
