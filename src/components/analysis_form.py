import streamlit as st
from services.ai_service import generate_analysis
from config.prompts import SPECIALIST_PROMPTS
from utils.pdf_extractor import extract_text_from_pdf
from config.sample_data import SAMPLE_REPORT
from config.app_config import MAX_UPLOAD_SIZE_MB
import requests
import re


def show_analysis_form():
    # Show last analysis result or error if present
    if st.session_state.get("last_analysis_result"):
        st.success(st.session_state.last_analysis_result)
        del st.session_state["last_analysis_result"]
    if st.session_state.get("last_analysis_error"):
        st.error(st.session_state.last_analysis_error)
        del st.session_state["last_analysis_error"]
        
    # Initialize report source in session state for new sessions
    if 'current_session' in st.session_state and 'report_source' not in st.session_state:
        st.session_state.report_source = "Upload PDF"
    
    report_source = st.radio(
        "Choose report source",
        ["Upload PDF", "Use Sample PDF"],
        index=0 if st.session_state.get('report_source') == "Upload PDF" else 1,
        horizontal=True,
        key='report_source'
    )

    pdf_contents = get_report_contents(report_source)
            
    if pdf_contents:  # Only show form if we have report content
        render_patient_form(pdf_contents)

def get_report_contents(report_source):
    if report_source == "Upload PDF":
        uploaded_file = st.file_uploader(
            f"Upload blood report PDF (Max {MAX_UPLOAD_SIZE_MB}MB)", 
            type=['pdf'],
            help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB}MB. Only PDF files containing medical reports are supported"
        )
        if uploaded_file:
            # Check file size before processing
            file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert to MB
            if file_size_mb > MAX_UPLOAD_SIZE_MB:
                st.error(f"File size ({file_size_mb:.1f}MB) exceeds the {MAX_UPLOAD_SIZE_MB}MB limit.")
                return None
                
            if uploaded_file.type != 'application/pdf':
                st.error("Please upload a valid PDF file.")
                return None
                
            pdf_contents = extract_text_from_pdf(uploaded_file)
            if isinstance(pdf_contents, str) and (
                pdf_contents.startswith(("File size exceeds", "Invalid file type", "Error validating")) or
                pdf_contents.startswith("The uploaded file") or
                "error" in pdf_contents.lower()
            ):
                st.error(pdf_contents)
                return None
            with st.expander("View Extracted Report"):
                st.text(pdf_contents)
            return pdf_contents
    else:
        with st.expander("View Sample Report"):
            st.text(SAMPLE_REPORT)
        return SAMPLE_REPORT
    return None

def render_patient_form(pdf_contents,report_filename=None):
    with st.form("analysis_form"):
        patient_name = st.text_input("Patient Name")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        if st.form_submit_button("Analyze Report"):
            handle_form_submission(patient_name, age, gender, pdf_contents,report_filename)

def handle_form_submission(patient_name, age, gender, pdf_contents,report_filename):
    if not all([patient_name, age, gender]):
        st.error("Please fill in all fields")
        return

    # Check rate limit first, outside of spinner
    can_analyze, error_msg = generate_analysis(None, None, check_only=True)
    if not can_analyze:
        st.error(error_msg)
        st.stop()
        return

    # Determine report type/filename
    report_type = "Sample Report"
    if st.session_state.get('report_source') == "Upload PDF":
        uploaded_file = st.session_state.get('uploaded_file')
        if uploaded_file:
            report_type = uploaded_file.name

    with st.spinner("Analyzing report..."):
        # Save user message and proceed with analysis
        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session['id'],
            f"Analyzing report for patient: {patient_name}"
        )
        
        # Generate analysis
        result = generate_analysis({
            "patient_name": patient_name,
            "age": age,
            "gender": gender,
            "report": pdf_contents
        }, SPECIALIST_PROMPTS["comprehensive_analyst"])
        
        if result["success"]:
            content = result["content"]
            if "model_used" in result:
                model_info = f"\n\n*Analysis generated using {result['model_used']}*"
                content += model_info

            # Split content into sections
            def extract_section(header, text):
                pattern = rf"\*\*{header}\*\*\s*(.*?)(?=\n\s*\*\*|$)"
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                return match.group(1).strip() if match else ""

            analysis_sections = {
                "What is good": extract_section("What is good", content),
                "Be Alert!": extract_section("Be Alert!", content),
                "Need to check!": extract_section("Need to check!", content)
            }

            # Prepare analysis record
            analysis_record = {
                "user_id": st.session_state.user["id"],
                "session_id": st.session_state.current_session["id"],
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "report_type": report_type,
                "analysis": analysis_sections
            }

            # Store in session_state
            if "analysis_history" not in st.session_state:
                st.session_state.analysis_history = []
            st.session_state.analysis_history.append(analysis_record)

            # Show the analysis as a formatted string in the UI
            formatted_content = (
                f"**What is good**\n{analysis_sections['What is good']}\n\n"
                f"**Be Alert!**\n{analysis_sections['Be Alert!']}\n\n"
                f"**Need to check!**\n{analysis_sections['Need to check!']}"
            )
            st.session_state.last_analysis_result = formatted_content

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session['id'],
                formatted_content,
                role='assistant'
            )
            st.rerun()
        else:
            st.session_state.last_analysis_error = result["error"]
            st.stop()
