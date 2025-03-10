import streamlit as st
import random
import time
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Predefined passages from novels, newspapers, literature
passages = [
    {
        "text": "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled...",
        "questions": [
            {
                "question": "What is the mood conveyed in the opening line?",
                "options": ["Optimistic", "Depressing", "Romantic", "Indifferent"],
                "answer": "Depressing"
            },
            {
                "question": "What does 'clocks striking thirteen' imply?",
                "options": ["Time is broken", "Military time", "Bad omen", "New Year"],
                "answer": "Military time"
            },
            # 8 more questions...
        ]
    },
    {
        "text": "The sun sank slowly, casting a warm glow on the horizon. The birds returned to their nests as the evening...",
        "questions": [
            {
                "question": "What is the setting of the passage?",
                "options": ["Morning", "Evening", "Afternoon", "Night"],
                "answer": "Evening"
            },
            {
                "question": "The tone of the passage is:",
                "options": ["Melancholic", "Peaceful", "Dramatic", "Humorous"],
                "answer": "Peaceful"
            },
            # 8 more questions...
        ]
    }
]

# Select a random passage
selected_passage = random.choice(passages)

# Streamlit UI
st.title("CUET English Reading Ability Mock Test")
st.write("Read the passage carefully and answer the following questions:")

# Display the passage
st.text_area("Passage:", value=selected_passage['text'], height=350)

# Generate and display 10 MCQs
user_answers = []
score = 0

for i, q in enumerate(selected_passage['questions']):
    st.write(f"Q{i+1}. {q['question']}")
    user_answer = st.radio(f"Choose one:", q['options'], key=f"answer_{i}")
    user_answers.append(user_answer)
    
    # Calculate score
    if user_answer == q['answer']:
        score += 1

# Countdown Timer
if st.button("Start Timer"):
    st.session_state.start_time = time.time()

if 'start_time' in st.session_state:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 1200 - elapsed_time
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    
    if remaining_time > 0:
        st.write(f"Time remaining: {minutes} minutes {seconds} seconds")
    else:
        st.warning("Time's up!")
        st.session_state.start_time = None

# Function to generate PDF report
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CUET English Mock Test Report", ln=True, align='C')
    
    # Add the passage
    pdf.multi_cell(0, 10, txt=f"Passage:\n\n{selected_passage['text']}\n\n")
    
    # Add questions, user answers, and correct answers
    for i, q in enumerate(selected_passage['questions']):
        pdf.multi_cell(0, 10, txt=f"Q{i+1}. {q['question']}")
        pdf.multi_cell(0, 10, txt=f"Your Answer: {user_answers[i]}")
        pdf.multi_cell(0, 10, txt=f"Correct Answer: {q['answer']}\n\n")
    
    # Add Score
    pdf.multi_cell(0, 10, txt=f"Your Score: {score}/10")
    
    # Save the PDF
    filename = f"CUET_MockTest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Button to download PDF
if st.button("Download Report"):
    filename = generate_pdf()
    with open(filename, "rb") as f:
        st.download_button("Download your report", f, file_name=filename)

# Reset Button
if st.button("Reset Test"):
    st.experimental_rerun()
