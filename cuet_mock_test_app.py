import streamlit as st
import random
import time
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to fetch random comprehension from Wikipedia
def get_random_comprehension():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    # Extract the first non-empty paragraph
    passage = ""
    for para in paragraphs:
        if len(para.text.strip()) > 100:
            passage = para.text.strip()
            break
    
    # Generate random questions
    questions = [
        {
            "question": f"What is the main topic of the passage?",
            "options": [
                "History of the event",
                "Scientific discovery",
                "Person's biography",
                "Geographic location"
            ],
            "answer": "Person's biography" if "born" in passage.lower() else "Scientific discovery"
        },
        {
            "question": f"Which of the following is most likely true about the passage?",
            "options": [
                "It describes a past event.",
                "It explains a scientific concept.",
                "It narrates a person's life.",
                "It discusses a place's importance."
            ],
            "answer": "It narrates a person's life." if "born" in passage.lower() else "It explains a scientific concept."
        }
    ]
    
    return {"passage": passage, "questions": questions}

# PDF Generation Function
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CUET English Mock Test Report', ln=True, align='C')

    def add_test_details(self, passage, user_answers, correct_answers):
        self.set_font('Arial', '', 12)
        self.ln(10)
        self.multi_cell(0, 10, f"Passage:\n{passage}\n")
        
        for i, (q, u_ans, c_ans) in enumerate(zip(passage["questions"], user_answers, correct_answers), start=1):
            self.ln(5)
            self.cell(0, 10, f"Q{i}. {q['question']}")
            self.ln(5)
            self.cell(0, 10, f"Your Answer: {u_ans}")
            self.ln(5)
            self.cell(0, 10, f"Correct Answer: {c_ans}")
            self.ln(10)

# Streamlit Interface
st.title("CUET English Mock Test")
st.write("Test your comprehension skills with a daily mock test!")

# Timer
test_time = 20 * 60  # 20 minutes
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

time_left = test_time - (time.time() - st.session_state['start_time'])

if time_left <= 0:
    st.warning("⏰ Time's up!")
    st.session_state['time_up'] = True
else:
    mins, secs = divmod(int(time_left), 60)
    st.write(f"⏳ **Time Remaining:** {mins} min {secs} sec")

# Mock Test Generation
if 'mock_test' not in st.session_state:
    st.session_state['mock_test'] = get_random_comprehension()

passage_data = st.session_state['mock_test']
st.write("### Passage:")
st.write(passage_data["passage"])

# Questions
user_answers = []
for i, q in enumerate(passage_data["questions"]):
    user_answer = st.radio(f"Q{i+1}. {q['question']}", q['options'], key=f"q{i}")
    user_answers.append(user_answer)

# Submit Button
if st.button("Submit Test"):
    correct_answers = [q["answer"] for q in passage_data["questions"]]
    score = sum([1 if user_ans == correct_ans else 0 for user_ans, correct_ans in zip(user_answers, correct_answers)])

    # Display Results
    st.success(f"✅ Test completed! You scored **{score}/{len(correct_answers)}**")

    # Generate PDF with Date in File Name
    pdf = PDF()
    pdf.add_page()
    pdf.add_test_details(passage_data, user_answers, correct_answers)
    
    # Generate a date-stamped file name
    today = datetime.now().strftime('%m-%d-%Y')
    pdf_file = f"{today}_Mock_Test_Report.pdf"
    pdf.output(pdf_file)

    # Download Link
    with open(pdf_file, "rb") as file:
        st.download_button("📥 Download PDF Report", file, file_name=pdf_file)

# Reset Button
if st.button("Reset Test"):
    st.session_state.clear()
    st.rerun()
