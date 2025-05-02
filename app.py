import streamlit as st1
import docx2txt
import PyPDF2
import io

def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return ""

def score_resume(resume_text, scoring_input):
    total_score = 0
    matched_keywords = []
    for keyword, weight in scoring_input.items():
        if keyword.lower() in resume_text.lower():
            total_score += weight
            matched_keywords.append(keyword)
    return total_score, matched_keywords

# --- Streamlit UI ---
st.title("📄 AI Resume Shortlisting Tool")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

st.subheader("🧠 Enter Scoring Keywords & Weights")
keywords = {}
for i in range(1, 6):
    col1, col2 = st.columns([2, 1])
    with col1:
        keyword = st.text_input(f"Keyword {i}", key=f"kw_{i}")
    with col2:
        weight = st.number_input(f"Weight {i}", min_value=1, max_value=100, key=f"wt_{i}")
    if keyword:
        keywords[keyword] = weight

threshold = st.number_input("🎯 Minimum Score to Shortlist", min_value=0, max_value=100, value=25)

if uploaded_file and keywords:
    resume_text = extract_text(uploaded_file)
    score, matched = score_resume(resume_text, keywords)
    st.markdown("---")
    st.subheader("✅ Results")
    st.write(f"**Score:** {score}")
    st.write(f"**Matched Keywords:** {matched}")
    st.success("Shortlisted ✅" if score >= threshold else "Not Shortlisted ❌")
