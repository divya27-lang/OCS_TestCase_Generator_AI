import streamlit as st
from app import run_pipeline

st.title("OCS Test Case Generator")

query = st.text_area(
    "Enter query",
    "Act as expert QA OCS test engineer and generate OCS test cases."
)

if st.button("Generate Test Cases"):

    with st.spinner("Processing..."):
        result, excel_file = run_pipeline(query)

    st.subheader("Generated Test Cases")
    st.text(result)

    # download button
    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name="testcases.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
