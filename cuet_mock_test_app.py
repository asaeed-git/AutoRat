import streamlit as st
import random
import time
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to fetch a long random passage from Wikipedia
def get_random_comprehension():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    # Combine multiple paragraphs to make a longer passage
    passage = ""
    for para in paragraphs:
        passage += para.text.strip() + " "
        if len(passage) > 1200:  # Ensure the passage is sufficiently long
            break
    return passage

# Function to generate 10 random questions
def generate_questions(passage):
    questions = []
    for i in range(10):
        questions.append(f"Q{i+1}. What is the main idea of the passage?")
    return questions

# Streamlit UI
st.title("CUET English Mock Test")
st.write("Read the passage carefully and answer the questions below:")

# Fetch a longer passage
passage = get_random_comprehension()
st.text_area("Passage:", value=passage, height=300)

# Generate 10 questions
questions = generate_questions(passage)
answers = []

# Display questions and text input for answers
for i, question in enumerate(questions):
    answer = st.text_input(question, key=f"answer_{i}")
    answers.append(answer)

# Countdown Timer
if st.button("Start Timer"):
    st.session_state.start_time = time.time()

if 'start_time' in st.session_state:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 1200 - elapsed_time
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    st.write(f"Time remaining: {minutes} minutes {seconds} seconds")
    if remaining_time <= 0:
        st.warning("Time's up!")
        st.session_state.start_time = None

# Generate PDF Function
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CUET English Mock Test Report", ln=True, align='C')
    
    pdf.multi_cell(0, 10, txt=f"Passage:\n{passage}")
    for i, question in enumerate(questions):
        pdf.multi_cell(0, 10, txt=f"{question}\nYour Answer: {answers[i]}\n\n")
    
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
