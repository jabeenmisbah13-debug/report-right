import os
import streamlit as st
from google import genai
from analyzer import analyze

MODEL = "gemini-3.1-flash-lite"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.title("ReportRight")
st.caption("Understand your lab report in simple words. Sample data only.")

report = st.text_area("Paste your lab report", height=200)

if st.button("Explain") and report:
    results = analyze(report)
    if results:
        st.table(results)
    flagged = "\n".join(
        f"{r['Test']}: {r['Value']} {r['Unit']} ({r['Status']})" for r in results
    )
    prompt = (
        "Explain this lab report in simple words for a non-medical person. "
        "Do not diagnose. These values were already checked by code:\n"
        + flagged
        + "\n\nExplain what each abnormal value could mean and which need "
        "a doctor's attention. Plain text, no asterisks.\n\n" + report
    )
    with st.spinner("Reading your report..."):
        resp = client.models.generate_content(model=MODEL, contents=prompt)
    st.write(resp.text)