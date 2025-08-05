# Resume Matcher 🎯

An AI-powered Resume Matcher built with Django and Natural Language Processing (NLP). This tool helps match resumes to job descriptions and calculates a match score with visual output.

## 🔥 Features

- Upload Resume (PDF)
- Upload Job Description (Text)
- AI gives a matching score
- Shows Pie Chart for visual results
- Login, Register, Logout functionality
- Match History page

## 🛠 Tech Stack

- Python
- Django
- HTML, CSS
- Chart.js
- SQLite3
- NLP (using spaCy or similar)

## 🚀 How to Run Locally

```bash
# Clone the project
git clone https://github.com/veena202826/resume_matcher.git
cd resume_matcher

# Create a virtual environment
python -m venv env
env\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt  # If you create one manually

# Run the server
python manage.py runserver
