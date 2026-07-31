import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

from gtts import gTTS
import tempfile

def ask_question(question):
    prompt = f"""
You are PGC Bot.

Answer this student's question clearly and simply.

Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_file.name)

    return temp_file.name
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-3.6-flash"


def ai_study_plan(name, program, subjects, weak_subjects,
                  preferred_time, study_hours, goal, exam_date):

    prompt = f"""
You are PGC Bot, an expert AI study planner.

Student Name: {name}
Program: {program}
Subjects: {subjects}
Weak Subjects: {weak_subjects}
Preferred Study Time: {preferred_time}
Study Hours Per Day: {study_hours}
Exam Date: {exam_date}
Target: {goal}

Create:
1. A personalized daily study schedule.
2. A weekly revision plan.
3. Break timings.
4. Study tips.
5. Motivation.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def ask_question(question):

    prompt = f"""
You are PGC Bot.

Answer this student's question clearly and simply.

Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def ask_pdf(pdf_text, question):

    prompt = f"""
You are PGC Bot.

Answer ONLY from the uploaded PDF.

PDF:
{pdf_text}

Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_mcqs(pdf_text, mcq_count):

    prompt = f"""
Generate {mcq_count} multiple choice questions from these notes.

Rules:
- Each MCQ must have 4 options (A, B, C, D)
- Give the correct answer.
- Give a short explanation.

PDF Notes:

{pdf_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
