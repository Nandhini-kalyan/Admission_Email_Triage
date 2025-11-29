Clone & install
git clone https://github.com/Nandhini-kalyan/Admission_Email_Triage.git
cd admissions_triage
uv sync #install uv for easier and  quicker package management

Add OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

Run
streamlit run app.py
