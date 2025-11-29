# Admissions Email Triage Assistant

AI-powered internal tool that reads parent/student enquiry emails, classifies them into useful categories, extracts key details, and produces a structured leads file for school admissions teams.

## Overview

This app is a small prototype of how AI can automate repetitive administrative work in a school group:

- Input: A CSV of emails (id, subject, body)
- Processing: An LLM classifies each email and extracts structured fields
- Output: A clean CSV of admissions leads, ready to be loaded into a CRM/ERP or viewed in the built-in dashboard

It is designed for non-technical users (admissions / admin staff) and runs as a simple Streamlit web app.

## Features

- Email classification into categories such as:
  - Admissions
  - Fees
  - Transport
  - Curriculum
  - Complaint
  - Sports
  - General / Other
- Priority tagging (High / Medium / Low)
- Entity extraction:
  - Student name
  - Grade applying for (or current grade)
  - Campus (e.g., Dubai, Abu Dhabi, Sharjah)
  - Contact details (phone / email)
- Interactive dashboard:
  - Summary metrics (total leads, high-priority, admissions count)
  - Filterable table by category
  - Downloadable CSV with structured leads

## Tech Stack

- Python
- Streamlit (UI)
- OpenAI API (GPT-4o-mini) for classification and extraction
- Pandas for CSV handling
- dotenv / environment variables for secret management

## How It Works

1. User uploads a CSV with columns:
   - id
   - subject
   - body

2. For each email, the app sends a prompt to the OpenAI model asking it to:
   - Classify the email into one of the predefined categories
   - Assign a priority (High / Medium / Low)
   - Extract key entities (student name, grade, campus, contact)
   - Return everything as strict JSON

3. The app aggregates all results into a Pandas DataFrame and:
   - Shows metrics and a filterable table in the UI
   - Allows export of the structured leads as a CSV file

4. This CSV can then be used for:
   - Admissions funnels
   - Follow-up workflows
   - Integration with CRM/ERP systems

## Setup

1. Clone the repository and move into the project folder:

- git clone https://github.com/Nandhini-kalyan/Admission_Email_Triage.git
- cd admissions_triage
- uv sync #install uv for easier and  quicker package management

2. Add OpenAI key
- echo "OPENAI_API_KEY=sk-..." > .env

3. Run
- uv run streamlit run app.py


## Usage

1. Open the Streamlit URL shown in the terminal (usually http://localhost:8501).
2. Either:
- Use the built-in sample emails, or
- Upload your own CSV with columns `id`, `subject`, `body`.
3. Click “Classify All Emails”.
4. Review:
- Summary metrics (total leads, high priority, admissions).
- Filtered table by category.
5. Download the structured leads CSV for further analysis or system integration.

## Sample screenshot

<img width="1362" height="632" alt="image" src="https://github.com/user-attachments/assets/82521cad-5d20-4c08-95ea-3a785eeff8e5" />

## Why This Is Relevant for a School Group

- Demonstrates how LLMs can sit on top of existing email workflows and reduce manual triage.
- Shows an internal, non-public tool pattern: a simple UI that staff can use without technical skills.
- Produces structured data that can feed into ERP/CRM, dashboards, or further automation.
- The same pattern can be reused for:
- HR resume triage
- Admissions form free-text fields
- Generic parent feedback and complaints routing

---

Author: Nandhini Kalyanasundaram  
Email: knandhini867@gmail.com  
LinkedIn: https://www.linkedin.com/in/nandhini-kalyanasundaram
