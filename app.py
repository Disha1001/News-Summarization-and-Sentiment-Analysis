import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000/analyze"
AUDIO_URL = "http://127.0.0.1:8000/audio/"

st.set_page_config(page_title="AI News Analysis", layout="centered")

st.title("News Summerization and TTS Application")

# Input for company name
company_name = st.text_input("Enter a company name:", "")

# Button to generate the report
if st.button("Generate Report"):
    with st.spinner("Fetching and analyzing news..."):
        response = requests.get(API_URL, params={"company": company_name})
        
        if response.status_code == 200:
            data = response.json()
            
            # Store data in session state to use later
            st.session_state["report_data"] = data
            st.session_state["report_ready"] = True
        else:
            st.error("Failed to fetch news analysis. Try again later.")
            st.session_state["report_ready"] = False

# Display report and download buttons only if the report is generated
if st.session_state.get("report_ready"):
    st.success("Report Generated Successfully!")

    # Download Report Button
    report_json = json.dumps(st.session_state["report_data"], indent=4)
    st.download_button(
        label="Download Report",
        data=report_json,
        file_name=f"{company_name}_news_report.json",
        mime="application/json"
    )

    # Download Audio Button 
    audio_url = st.session_state["report_data"].get("Audio")
    if audio_url:
        st.download_button(
            label="Download Audio",
            data=requests.get(AUDIO_URL + company_name).content,
            file_name=f"{company_name}_report_hindi.mp3",
            mime="audio/mpeg"
        )
