import subprocess
import sys

# Force install required packages for cloud deployment
subprocess.run(
    [sys.executable, "-m", "pip", "install", "groq", "pypdf", "pydantic", "python-dotenv"],
    capture_output=True
)

import streamlit as st
import pandas as pd
from extractor import extract_financial_data, extract_multiple_companies
from pypdf import PdfReader

# Page config
st.set_page_config(
    page_title="FinExtract",
    page_icon="💰",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("💰 FinExtract")
    st.markdown("---")
    st.markdown("### How to use")
    st.write("1. Paste financial text OR upload PDF")
    st.write("2. Choose single or multiple company mode")
    st.write("3. Click Extract KPIs")
    st.write("4. View and download results")
    st.markdown("---")
    st.markdown("### About")
    st.write("Built with Groq LLaMA3 + Pydantic + Streamlit")
    st.markdown("---")
    
    # Mode selector
    mode = st.radio(
        "Extraction Mode",
        ["Single Company", "Multiple Companies"],
        help="Multiple Companies mode finds all companies in your text"
    )

# Main area
st.title("FinExtract 💰")
st.subheader("Extract structured financial KPIs from any text using AI")

# Two tabs
tab1, tab2 = st.tabs(["📝 Paste Text", "📄 Upload PDF"])

with tab1:
    user_input = st.text_area(
        "Paste financial text here",
        height=250,
        placeholder="Example: Reliance Industries reported revenue of 2.31 lakh crore for Q3 2024, up 10.4% YoY..."
    )
    
    if st.button("Extract KPIs", type="primary", key="extract_text"):
        if user_input:
            with st.spinner("Extracting financial data using AI..."):
                try:
                    if mode == "Single Company":
                        result = extract_financial_data(user_input)
                        
                        # Use new to_display_dict method
                        display_data = result.to_display_dict()
                        df = pd.DataFrame([display_data])
                        
                        # Show summary line
                        st.info(f"📊 {result.summary()}")
                        st.success("Extraction Complete!")
                        st.dataframe(df, use_container_width=True)
                        
                    else:
                        # Multiple companies mode
                        results = extract_multiple_companies(user_input)
                        
                        if results:
                            all_data = [r.to_display_dict() for r in results]
                            df = pd.DataFrame(all_data)
                            
                            st.success(f"Found {len(results)} companies!")
                            for r in results:
                                st.info(f"📊 {r.summary()}")
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("No company data found in text")
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download as CSV",
                        csv,
                        "financial_data.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
                    st.info("Try rephrasing the text or check if it contains financial data")
        else:
            st.warning("Please paste some financial text first!")

with tab2:
    uploaded_file = st.file_uploader(
        "Upload a financial PDF report",
        type="pdf",
        help="Upload any earnings report or financial news PDF"
    )
    
    if uploaded_file:
        st.info(f"📄 File uploaded: {uploaded_file.name}")
        
        if st.button("Extract from PDF", type="primary", key="extract_pdf"):
            with st.spinner("Reading PDF..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([
                    page.extract_text()
                    for page in reader.pages
                    if page.extract_text()
                ])
                st.info(f"Extracted {len(text)} characters from PDF")
            
            with st.spinner("Extracting KPIs using AI..."):
                try:
                    result = extract_financial_data(text)
                    display_data = result.to_display_dict()
                    df = pd.DataFrame([display_data])
                    
                    st.info(f"📊 {result.summary()}")
                    st.success("Extraction Complete!")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        "financial_data.csv"
                    )
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 10px;'>
        Built by <b>Bhavna</b> | 
        <a href='https://github.com/BHAVNA510' target='_blank'>GitHub</a> | 
        <a href='https://www.linkedin.com/in/bhavna51020' target='_blank'>LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)