import streamlit as st
import random
import time
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to fetch a long unseen passage
def get_random_comprehension():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    # Combine paragraphs until the passage length is long enough
    passage = ""
    for para in paragraphs:
        text = para.text.strip()
        if text:
            passage += text + " "
        if len(passage.split()) > 250:  # Ensure passage has 250+ words
            break
    
    # Clean the passage
    passage = passage.replace('\n', ' ').strip()
    return passage

# Function to generate 10 comprehension questions
def generate_questions(passage):
    questions = [
        "What is the main theme of the passage?",
        "Which of the following best summarizes the passage?",
        "What can be inferred from the passage?",
        "What is the tone of the passage?",
        "According to the passage, which statement is true?",
        "Which of the following is a suitable title for the passage?",
        "What is the primary purpose of the author?",
        "Find the meaning of the word ‘____’ from the passage.",
        "Which of the following best describes the author's attitude?",
        "Identify the correct interpretation of the last paragraph."
    ]
    return questions

# Streamlit UI
st.title("CUET English Reading Ability Mock Test")
st.write("Read the passage carefully and answer the following questions:")

# Fetch long unseen passage
passage = get_random_comprehension()
st.text_area("Passage:", value=passage, height=350)

# Generate and display 10 questions
questions = generate_questions(passage)
answers = []

for i, question in enumerate(questions):
    answer = st.text_input(f"{i+1}. {question}", key=f"answer_{i}")
    answers.append(answer)

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
    pdf.multi_cell(0, 10, txt=f"Passage:\n\n{passage}\n\n")
    
    # Add questions and answers
    for i, question in enumerate(questions):
        pdf.multi_cell(0, 10, txt=f"Q{i+1}. {question}\nYour Answer: {answers[i]}\n\n")
    
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
