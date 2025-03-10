import streamlit as st
import random
import time
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to fetch unseen passage from the internet
def get_live_passage():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    # Combine multiple paragraphs to form a long passage
    passage = ""
    for para in paragraphs:
        text = para.text.strip()
        if text:
            passage += text + " "
        if len(passage.split()) > 300:  # Ensure passage has 300+ words
            break
    
    passage = passage.replace('\n', ' ').strip()
    return passage

# Function to auto-generate 10 questions from passage
def generate_questions(passage):
    questions = []
    for i in range(10):
        question = f"What is the main idea of the passage?"
        options = ["Option A", "Option B", "Option C", "Option D"]
        correct_answer = random.choice(options)
        questions.append({
            "question": question,
            "options": options,
            "answer": correct_answer
        })
    return questions

# Fetch passage
passage = get_live_passage()

# Streamlit UI
st.title("CUET English Reading Ability Mock Test")
st.write("Read the passage carefully and answer the following questions:")

# Display Passage
st.text_area("Passage:", value=passage, height=350)

# Generate and display 10 MCQs
user_answers = []
questions = generate_questions(passage)
score = 0

for i, q in enumerate(questions):
    st.write(f"Q{i+1}. {q['question']}")
    user_answer = st.radio("Choose one:", q['options'], key=f"answer_{i}")
    user_answers.append(user_answer)
    
    # Check if the answer is correct
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
    
    # Add passage
    pdf.multi_cell(0, 10, txt=f"Passage:\n\n{passage}\n\n")
    
    # Add questions and answers
    for i, q in enumerate(questions):
        pdf.multi_cell(0, 10, txt=f"Q{i+1}. {q['question']}")
        pdf.multi_cell(0, 10, txt=f"Your Answer: {user_answers[i]}")
        pdf.multi_cell(0, 10, txt=f"Correct Answer: {q['answer']}\n\n")
    
    # Add Score
    pdf.multi_cell(0, 10, txt=f"Your Score: {score}/10")
    
    # Save PDF
    filename = f"CUET_MockTest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Download Report Button
if st.button("Download Report"):
    filename = generate_pdf()
    with open(filename, "rb") as f:
        st.download_button("Download your report", f, file_name=filename)

# Reset Button
if st.button("Reset Test"):
    st.experimental_rerun()
