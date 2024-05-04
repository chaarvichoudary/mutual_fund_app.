import streamlit as st
import pandas as pd
from PyPDF2 import PdfFileReader
import tabula

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as f:
        reader = PdfFileReader(f)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

# Function to extract tables from PDF
def extract_tables_from_pdf(pdf_file):
    return tabula.read_pdf(pdf_file, pages='all')

# Function to calculate derived fields
def calculate_derived_fields(df):
    df['Net Inflow/Outflow'] = df['Funds Mobilized'] - df['Repurchase/Redemption']
    df['Net AUM per Scheme'] = df['Net Assets Under Management'] / df['No. of Schemes']
    df['Net Inflow/Outflow per Scheme'] = df['Net Inflow/Outflow'] / df['No. of Schemes']
    return df

# Main function to run the Streamlit app
def main():
    st.title('Mutual Fund Data Analysis App')

    # Data upload functionality
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        pdf_tables = extract_tables_from_pdf(uploaded_file)

        # Display extracted text
        st.subheader("Extracted Text from PDF")
        st.write(pdf_text)

        # Display extracted tables
        st.subheader("Extracted Tables from PDF")
        for i, table in enumerate(pdf_tables):
            st.write(f"Table {i+1}")
            st.write(table)

        # Scheme selection
        schemes = st.multiselect("Select Mutual Fund Schemes", pdf_tables[0].columns.tolist())

        # Field selection
        fields = st.multiselect("Select Data Fields", pdf_tables[0].columns.tolist())

        # Calculate derived fields
        df = calculate_derived_fields(pdf_tables[0])

        # Filter data based on scheme and field selection
        df = df[schemes + fields]

        # Display dynamic report
        st.subheader("Generated Report")
        st.write(df)

        # Download report as CSV
        csv_data = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv_data, file_name='mutual_fund_report.csv', mime='text/csv')

if __name__ == "__main__":
    main()
