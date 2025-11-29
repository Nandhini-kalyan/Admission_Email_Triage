Clone & install
git clone 
cd admissions_triage
uv sync #install uv for easier and  quicker package management

Add OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

Run
streamlit run app.py
