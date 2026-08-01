from ai import ai_study_plan, ask_question, ask_pdf, generate_mcqs, text_to_speech
import streamlit as st
from datetime import date
import fitz
from streamlit_mic_recorder import speech_to_text
import base64

def add_bg():
    with open("pic.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #6dd5ed, #2193b0, #6a11cb);
    background-attachment: fixed;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.15);
}

div[data-baseweb="input"] {
    background-color: white;
    border-radius: 10px;
}

/* Date picker */
div[data-testid="stDateInput"] input {
    background-color: white;
    color: black;
    border-radius: 10px;
}

div[data-testid="stDateInput"] button {
    color: black;
}

button[kind="primary"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title("🎓 PGC Bot")
st.write("""
Welcome to *PGC Bot*, your personal AI study assistant.
""")

st.markdown("---")
st.header("🎤 Voice Assistant")

# voice_question = speech_to_text(
#     language="en",
#     use_container_width=True,
#     just_once=True,
#     key="voice"
# )
voice = speech_to_text(
    language="en",
    use_container_width=True,
    just_once=True,
    key="voice"
)

if voice:

    st.write("🎤 You said:", voice)

    with st.spinner("🤖 Thinking..."):

        answer = ask_question(voice)

    st.write(answer)

    audio = text_to_speech(answer)

    st.audio(audio)



# ==========================
# Student Information
# ==========================

st.header("🧑 Student Information")

name = st.text_input("Student Name")
program = st.selectbox(
    "Select Program",
    ["FSc Pre-Medical", "FSc Pre-Engineering", "ICS", "ICOM", "FA"]
)

subjects = st.text_area(
    "Subjects",
    placeholder="Biology, Chemistry, Physics"
)

weak_subjects = st.text_input(
    "Weak Subjects",
    placeholder="Chemistry, Physics"
)

preferred_time = st.selectbox(
    "Preferred Study Time",
    ["Morning", "Afternoon", "Evening", "Night"]
)

exam_date = st.date_input(
    "Exam Date",
    min_value=date.today()
)

study_hours = st.slider(
    "Daily Study Hours",
    1,
    12,
    4
)

goal = st.text_area(
    "Target",
    placeholder="I want to score above 90%."
)

# ==========================
# AI Study Plan
# ==========================

if st.button("📅 Generate AI Study Plan"):

    with st.spinner("🤖 Generating your study plan..."):

        plan = ai_study_plan(
            name,
            program,
            subjects,
            weak_subjects,
            preferred_time,
            study_hours,
            goal,
            exam_date
        )

    st.success("✅ Study Plan Generated!")

    st.markdown("## 📚 Your AI Study Plan")
    st.write(plan)

    st.download_button(
        "📥 Download Study Plan",
        data=plan,
        file_name="StudyPlan.txt",
        mime="text/plain"
    )

# ==========================
# Ask AI
# ==========================

st.markdown("---")
st.header("💬 Ask PGC Bot")

question = st.text_input(
    "Ask any study-related question"
)

if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 Thinking..."):

            answer = ask_question(question)
            st.write(answer)
            audio_file = text_to_speech(answer)
            st.audio(audio_file)

     #   st.markdown("### 📖 Answer")
     #   st.write(answer)

# ==========================
# PDF Upload
# ==========================

st.markdown("---")
st.header("📄 Upload PDF Notes")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf"
)

pdf_text = ""

if uploaded_file is not None:

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in doc:
        pdf_text += page.get_text()

    st.success("✅ PDF Uploaded Successfully!")

    pdf_question = st.text_input(
        "Ask a question from the uploaded PDF"
    )

    if st.button("Ask PDF"):

        with st.spinner("🤖 Reading PDF..."):

            pdf_answer = ask_pdf(
                pdf_text,
                pdf_question
            )

        st.markdown("### 📄 PDF Answer")
        st.write(pdf_answer)
        st.markdown("## 📝 Generate MCQs")
st.markdown("---")
st.markdown("## 📝 Generate MCQs")

mcq_count = st.selectbox(
    "Number of MCQs",
    [5, 10, 20, 30],
    index=1
)

if st.button("Generate MCQs"):

    with st.spinner("🤖 Creating MCQs..."):

        mcqs = generate_mcqs(
            pdf_text,
            mcq_count
        )

    st.markdown("## 📝 Generate MCQs")
    st.write(mcqs)

    st.download_button(
        "📥 Download MCQs",
        data=mcqs,
        file_name="MCQs.txt",
        mime="text/plain"
    )
