import os, json
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine
from crew.main_call import main

# Function to process text from images using OCR (Tesseract)
def extract_text_from_image(image):
    """Extracts text from an image using Tesseract OCR. 
    but in long term, we should use Google Vision API.
    """
    text = pytesseract.image_to_string(image)
    return text

# Function to read Excel data (assets/liabilities and bank statement)
def read_excel_file(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

def connect_to_postgres(uri: str):
    """Connects to a PostgreSQL database using the provided URI."""
    engine = create_engine(uri)
    return engine

def load_data_to_db(df: pd.DataFrame, db_url: str, table_name: str):
    """Loads a DataFrame into a PostgreSQL database."""
    if not db_url:
        raise ValueError("Database URL is not provided.")
    engine = create_engine(db_url)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Function to handle the interactive chat
def chat_interaction(applicant_data):
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Applicant Data: "+ str(applicant_data)}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = main(st.session_state.messages)
        msg = str(response)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

# Main App
def chat_main():
    st.title("Social Support Application")
    st.caption("🚀 A chatbot created by Abhishek")

    # Step 1: Manual Data Entry
    st.header("Enter Applicant Information")
    income = st.number_input("Income", min_value=0.0, step=1000.0)
    family_size = st.number_input("Family Size", min_value=1, max_value=10)
    address = st.text_input("Address")
    employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-Employed"])
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850)
    assets_liabilities = st.number_input("Assets to Liabilities Ratio", min_value=0.0, step=0.1)

    applicant_data = {
        "income": income,
        "family_size": family_size,
        "address": address,
        "employment_status": employment_status,
        "credit_score": credit_score,
        "assets_liabilities_ratio": assets_liabilities
    }

    # Step 2: Upload Documents
    st.header("Upload Documents")

    uploaded_emirates_id = st.file_uploader("Upload Emirates ID (Image)", type=["jpg", "jpeg", "png"])
    uploaded_bank_statement = st.file_uploader("Upload Bank Statement (Excel)", type=["xlsx"])
    uploaded_resume = st.file_uploader("Upload Resume (PDF/Word)", type=["pdf", "docx"])
    uploaded_assets_liabilities = st.file_uploader("Upload Assets/Liabilities (Excel)", type=["xlsx"])
    uploaded_credit_report = st.file_uploader("Upload Credit Report (Excel)", type=["xlsx"])

    # Step 3: Process the Emirates ID image (OCR)
    if uploaded_emirates_id is not None:
        image = Image.open(uploaded_emirates_id)
        emirates_id_text = extract_text_from_image(image)
        st.write("Emirates ID Text:", emirates_id_text)
        applicant_data['emirates_id_text'] = emirates_id_text

    # Step 4: Process the Bank Statement and Assets/Liabilities Excel files
    if uploaded_bank_statement is not None:
        bank_statement_data = read_excel_file(uploaded_bank_statement)
        st.write("Bank Statement Data:", bank_statement_data)
        applicant_data['bank_statement_data'] = bank_statement_data

    if uploaded_assets_liabilities is not None:
        assets_liabilities_data = read_excel_file(uploaded_assets_liabilities)
        st.write("Assets & Liabilities Data:", assets_liabilities_data)
        applicant_data['assets_liabilities_data'] = assets_liabilities_data

    if uploaded_credit_report is not None:
        uploaded_credit_report = read_excel_file(uploaded_credit_report)
        st.write("Uploaded Credit Report:", uploaded_credit_report)
        applicant_data['uploaded_credit_report'] = uploaded_credit_report

    # Step 5: Submit Button
    if st.button("Submit Application"):
        st.write("Application Submitted Successfully!")
        msg = str(main(applicant_data))
        # Further backend processing (e.g., saving to DB, further validation, etc.) can be added here.

    # Step 6: Display the interactive chat
    st.header("Interactive Chat")
    chat_interaction(msg)

if __name__ == "__main__":
    chat_main()
