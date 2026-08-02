import os
import tempfile
import fitz
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS

load_dotenv()

# ==========================
# Gemini Configuration
# ==========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-2.5-flash-lite"

# ==========================
# Text To Speech
# ==========================

def text_to_speech(text):
    tts = gTTS(
        text=text,
        lang="en"
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_file.name)

    return temp_file.name

# ==========================
# Read PDF using Gemini Vision
# ==========================

def read_pdf_with_gemini(uploaded_file):

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    full_text = ""

    for page in doc:

        pix = page.get_pixmap(dpi=300)
        image_bytes = pix.tobytes("png")

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    """
You are an AI OCR assistant.

Read every visible element on this PDF page.

Extract:
- Printed text
- Handwritten text
- Tables
- Graphs
- Charts
- Diagrams
- Mathematical equations
- Labels
- Captions
- Text inside images

Preserve the reading order.

Return only the extracted educational content as plain text.
""",
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/png"
                    )
                ]
            )

            if response.text:
                full_text += response.text + "\n\n"

        except Exception as e:
            full_text += f"\n[Error reading page: {e}]\n"

    doc.close()

    return full_text

    # ==========================
# AI Study Planner
# ==========================

def ai_study_plan(
    name,
    program,
    subjects,
    weak_subjects,
    preferred_time,
    study_hours,
    goal,
    exam_date
):

    prompt = f"""
You are PGC Bot, an expert study planner.

Create a complete personalized study plan.

Student Name: {name}
Program: {program}
Subjects: {subjects}
Weak Subjects: {weak_subjects}
Preferred Study Time: {preferred_time}
Study Hours Per Day: {study_hours}
Exam Date: {exam_date}
Target: {goal}

Generate:

1. Daily timetable
2. Weekly study plan
3. Revision schedule
4. Break timings
5. Smart study tips
6. Exam preparation strategy
7. Motivation
"""

    for attempt in range(3):
    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        if "503" in str(e):
            time.sleep(5)
            continue

        return f"❌ Error generating study plan:\n\n{e}"

return "⚠️ Gemini server is busy. Please try again."


# ==========================
# Ask AI
# ==========================

def ask_question(question):

    prompt = f"""
You are PGC Bot.

Answer the student's question clearly.

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

        return f"❌ Error:\n\n{e}"


# ==========================
# Ask Questions from PDF
# ==========================

def ask_pdf(pdf_text, question):

    prompt = f"""
You are PGC Bot.

Use ONLY the information extracted from the uploaded PDF.

If the answer is not available in the PDF, reply:

"I couldn't find this information in the uploaded PDF."

PDF Content:

{pdf_text}

Student Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error:\n\n{e}"


# ==========================
# Generate AI MCQs
# ==========================

def generate_mcqs(pdf_text, mcq_count):

    prompt = f"""
You are an expert teacher.

Generate exactly {mcq_count} multiple-choice questions from these notes.

Requirements:

• 4 options (A, B, C, D)
• Only one correct answer
• Mention the correct option
• Give a short explanation
• Cover different topics
• Use clear formatting

PDF Notes:

{pdf_text}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error:\n\n{e}"


# ==========================
# Helper Functions
# ==========================

def check_api_connection():
    """
    Check whether the Gemini API is working.
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with only the word: Connected"
        )

        return True, response.text

    except Exception as e:
        return False, str(e)


def summarize_notes(pdf_text):
    """
    Generate a concise summary of the extracted notes.
    """

    prompt = f"""
You are PGC Bot.

Summarize the following notes.

Include:
- Main topics
- Important concepts
- Key points
- Exam tips

Notes:

{pdf_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error:\n\n{e}"


def generate_flashcards(pdf_text):
    """
    Generate flashcards from notes.
    """

    prompt = f"""
Create flashcards from these notes.

Format:

Q: Question

A: Answer

Notes:

{pdf_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error:\n\n{e}"
