import streamlit as st
import pandas as pd
from extractor import extract_financial_data
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
    st.write("2. Click Extract KPIs")
    st.write("3. View and download results")
    st.markdown("---")
    st.write("Built with Groq + Streamlit")

# Main area
st.title("FinExtract 💰")
st.subheader("Extract structured financial KPIs from any text")

# Two tabs
tab1, tab2 = st.tabs(["📝 Paste Text", "📄 Upload PDF"])

with tab1:
    user_input = st.text_area(
        "Paste financial text here",
        height=250,
        placeholder="Example: Reliance Industries reported revenue of 2.31 lakh crore for Q3 2024..."
    )
    
    if st.button("Extract KPIs", type="primary"):
        if user_input:
            with st.spinner("Extracting financial data..."):
                try:
                    result = extract_financial_data(user_input)
                    df = pd.DataFrame([result.dict()])
                    
                    st.success("Extraction Complete!")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download as CSV",
                        csv,
                        "financial_data.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please paste some text first!")

with tab2:
    uploaded_file = st.file_uploader(
        "Upload a financial PDF",
        type="pdf"
    )
    
    if uploaded_file:
        if st.button("Extract from PDF", type="primary"):
            with st.spinner("Reading PDF..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([
                    page.extract_text()
                    for page in reader.pages
                ])
            
            with st.spinner("Extracting KPIs..."):
                try:
                    result = extract_financial_data(text)
                    df = pd.DataFrame([result.dict()])
                    
                    st.success("Extraction Complete!")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        "financial_data.csv"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
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