import streamlit as st
import pandas as pd
import openai
import os
import json
from datetime import datetime
import time

# Set page config
st.set_page_config(page_title="Admissions Email Triage", layout="wide")

# OpenAI setup
from dotenv import load_dotenv
load_dotenv(override=True)
openai.api_key = os.getenv('OPENAI_API_KEY')

MODEL = "gpt-4o-mini"

@st.cache_data
def load_sample_data():
    """Load sample emails for demo"""
    return pd.read_csv("sample_emails.csv")

def classify_email(email_text, subject):
    """Classify email and extract entities using OpenAI"""
    prompt = f"""
    Analyze this school admissions email and extract structured information.

    EMAIL SUBJECT: {subject}
    EMAIL BODY: {email_text}

    Return ONLY valid JSON with this exact schema:
    {{
        "category": "Admissions|Fees|Transport|Curriculum|Complaint|Sports|General|Other",
        "priority": "High|Medium|Low",
        "student_name": "name or null",
        "grade_applying_for": "grade or null", 
        "campus": "Dubai|Abu Dhabi|Sharjah|null",
        "contact_details": "phone/email or null",
        "summary": "1-sentence summary"
    }}

    Examples:
    - Admissions inquiry → category: "Admissions", priority: "High"
    - Fee payment issue → category: "Fees", priority: "High" 
    - General question → category: "General", priority: "Medium"
    """
    
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert school admissions assistant. Always return valid JSON matching the exact schema provided. Never add extra fields."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Classification error: {e}")
        return None

def main():
    st.title("Admissions Email Triage Assistant")
    st.markdown("**AI-powered tool to classify parent enquiries, extract key details, and create structured leads for admissions teams.**")
    
    # Sidebar
    st.sidebar.header("Demo Options")
    use_sample = st.sidebar.checkbox("Use Sample Emails", value=True)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Emails")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv", 
                                       help="CSV with columns: id, subject, body")
        
        if use_sample and not uploaded_file:
            df = load_sample_data()
            st.success(f"Loaded {len(df)} sample emails")
        elif uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} emails from upload")
        else:
            st.warning("Upload CSV or use sample data")
            st.stop()
    
    with col2:
        st.header("Processing")
        if st.button("Classify All Emails", type="primary"):
            progress_bar = st.progress(0)
            results = []
            
            for idx, row in df.iterrows():
                with st.spinner(f"Processing {row['subject'][:50]}..."):
                    result = classify_email(row['body'], row['subject'])
                    if result:
                        result['id'] = row['id']
                        result['subject'] = row['subject']
                        results.append(result)
                
                progress = min(1.0, (idx + 1) / len(df))
                progress_bar.progress(progress)

                time.sleep(0.1)  # Visual feedback
            
            # Save results
            results_df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"admissions_leads_{timestamp}.csv"
            results_df.to_csv(filename, index=False)
            
            st.session_state.results = results_df
            st.session_state.filename = filename
            st.success(f"Processed {len(results)} emails! Download: {filename}")
    
    # Results
    if 'results' in st.session_state:
        st.header("Structured Leads")
        df_results = st.session_state.results
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Leads", len(df_results))
        with col2:
            high_priority = len(df_results[df_results['priority'] == 'High'])
            st.metric("High Priority", high_priority)
        with col3:
            admissions = len(df_results[df_results['category'] == 'Admissions'])
            st.metric("Admissions", admissions)
        
        # Filterable table
        st.subheader("Filter & Review")
        category_filter = st.multiselect("Filter by Category", 
                                       df_results['category'].unique(),
                                       default=df_results['category'].unique())
        
        filtered_df = df_results[df_results['category'].isin(category_filter)]
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download CSV",
                data=st.session_state.results.to_csv(index=False),
                file_name=st.session_state.filename,
                mime="text/csv"
            )
        with col2:
            st.markdown(f"**Output format:** Ready for CRM/ERP import")

if __name__ == "__main__":
    main()
