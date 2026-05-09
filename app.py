
import streamlit as st
import pandas as pd
import random

# Load dataset
df = pd.read_csv("interview_questions.csv")

# Function to get random question
def get_question(role):

    filtered = df[df['role'] == role]

    row = filtered.sample(1).iloc[0]

    return row['question'], row['expected_keywords']

# Function to analyze answer
def analyze_answer(answer, keywords):

    score = 0

    answer = answer.lower()

    keyword_list = keywords.split(",")

    matched_keywords = []

    for word in keyword_list:

        if word.strip().lower() in answer:

            score += 2

            matched_keywords.append(word.strip())

    length_score = min(len(answer.split()) // 5, 4)

    total_score = score + length_score

    if total_score > 10:
        total_score = 10

    return total_score, matched_keywords

# Feedback function
def generate_feedback(score):

    if score >= 8:
        return "Excellent Answer! Very professional."

    elif score >= 5:
        return "Good Answer, but improve explanation."

    else:
        return "Try to explain with more technical detail."

# Streamlit UI
st.set_page_config(page_title="AI Interview Bot")

st.title("🤖 AI Interview Preparation Bot")

st.write("Practice technical interview questions using AI.")

# Role selection
role = st.selectbox(
    "Select Job Role",
    [
        "Data Scientist",
        "Python Developer",
        "Cyber Security",
        "AI Engineer",
        "Software Engineer"
    ]
)

# Generate Question
if st.button("Generate Question"):

    question, keywords = get_question(role)

    st.session_state.question = question

    st.session_state.keywords = keywords

# Show Question
if "question" in st.session_state:

    st.subheader("Interview Question")

    st.write(st.session_state.question)

    answer = st.text_area("Write Your Answer")

    # Analyze Answer
    if st.button("Analyze Answer"):

        score, matched = analyze_answer(
            answer,
            st.session_state.keywords
        )

        feedback = generate_feedback(score)

        st.success(f"Score: {score}/10")

        st.info(feedback)

        st.write("✅ Matched Keywords:")

        st.write(matched)
