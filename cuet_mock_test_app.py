import streamlit as st
import random
import time
from fpdf import FPDF

# Sample passages and questions
passages = [
    {
        "passage": "The industrial revolution, which began in the 18th century, significantly changed the landscape of labor and economy. Factories emerged as centers of production, introducing mechanized processes that increased efficiency but often led to poor working conditions.",
        "questions": [
            {"question": "When did the industrial revolution begin?", "options": ["17th century", "18th century", "19th century", "20th century"], "answer": "18th century"},
            {"question": "What was a major outcome of the industrial revolution?", "options": ["Increased agricultural productivity", "Emergence of factories", "Decline in trade", "Rise of monarchy"], "answer": "Emergence of factories"},
        ]
    },
    {
        "passage": "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water. This crucial process helps maintain the balance of oxygen in the Earth's atmosphere.",
        "questions": [
            {"question": "What do plants use in photosynthesis?", "options": ["Oxygen and water", "Sunlight and nitrogen", "Carbon dioxide and water", "Hydrogen and carbon"], "answer": "Carbon dioxide and water"},
            {"question": "What is the primary purpose of photosynthesis?", "options": ["To produce oxygen", "To synthesize nutrients", "To absorb heat", "To release carbon dioxide"], "answer": "To synthesize nutrients"},
        ]
    }
]

# Function to generate a random comprehension and questions
def generate_mock_test():
    selected_passage = random.choice(passages)
    return selected_passage

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
    st.session_state['mock_test'] = generate_mock_test()

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

    # Generate PDF
    pdf = PDF()
    pdf.add_page()
    pdf.add_test_details(passage_data, user_answers, correct_answers)
    pdf_file = "Mock_Test_Report.pdf"
    pdf.output(pdf_file)

    # Download Link
    with open(pdf_file, "rb") as file:
        st.download_button("📥 Download PDF Report", file, file_name=pdf_file)

# Reset Button
if st.button("Reset Test"):
    st.session_state.clear()
    st.rerun()

