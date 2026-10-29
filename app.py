import os
import streamlit as st
from google import genai

MODEL = "gemini-3.1-flash-lite"

st.set_page_config(
    page_title="ReportRight",
    page_icon="🩺",
    layout="centered"
)

st.title("ReportRight")
st.caption("Understand your lab report in simple words.")

st.info(
    "Medical disclaimer: ReportRight provides educational explanations, "
    "not medical diagnoses. Always discuss your results with a qualified "
    "healthcare professional."
)

st.caption("Use sample or anonymized report data while testing.")

report = st.text_area(
    "Paste your lab report",
    height=200,
    placeholder="Paste your test names, values, units, and reference ranges here..."
)

if st.button("Explain report", type="primary"):
    if not report.strip():
        st.warning("Please paste a lab report before clicking Explain.")
    else:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error(
                "The AI service is not configured. Please check "
                "the GEMINI_API_KEY environment variable."
            )
        else:
            prompt = (
                "Explain this laboratory report in simple language for a "
                "non-medical reader. Do not diagnose or prescribe treatment. "
                "Use reference ranges provided in the report when available. "
                "Do not invent reference ranges or assume a value is abnormal "
                "without sufficient information. Explain which results appear "
                "outside the provided ranges, if any, and suggest discussing "
                "unclear or abnormal results with a qualified healthcare "
                "professional. Mention that interpretation depends on the "
                "person's age, symptoms, medical history, and other factors. "
                "If information is missing, say so. Use clear headings and "
                "plain text.\n\n"
                "LAB REPORT:\n"
                + report.strip()
            )

            try:
                client = genai.Client(api_key=api_key)

                with st.spinner("Reading your report..."):
                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                if response.text and response.text.strip():
                    st.subheader("Your report explained")
                    st.write(response.text)
                    st.caption(
                        "This explanation is for educational purposes only. "
                        "Please review your results with your healthcare "
                        "professional."
                    )
                else:
                    st.warning(
                        "The AI returned an empty response. Please try again."
                    )

            except Exception:
                st.error(
                    "We couldn't analyse your report right now. "
                    "Please try again shortly. If the problem continues, "
                    "check your API configuration and terminal for errors."
                )