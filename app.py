import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib
import pdfplumber

try:
    resume_df = pd.read_csv("resume_data.csv")
    st.sidebar.success("✅ resume_data.csv loaded")
except Exception as e:
    st.sidebar.error(f"resume_data.csv: {e}")

try:
    salary_df = pd.read_csv("ds_salaries.csv")
    st.sidebar.success("✅ ds_salaries.csv loaded")
except Exception as e:
    st.sidebar.error(f"ds_salaries.csv: {e}")

try:
    jobs_df = pd.read_csv("DataAnalyst.csv.zip", compression="zip")
    st.sidebar.success("✅ DataAnalyst.csv.zip loaded")
except Exception as e:
    st.sidebar.error(f"DataAnalyst.csv.zip: {e}")

try:
    people_df = pd.read_csv("01_people.csv")
    st.sidebar.success("✅ 01_people.csv loaded")
except Exception as e:
    st.sidebar.error(f"01_people.csv: {e}")
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Screening & Job Market Analytics",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# APPLICATION TITLE
# =========================================================

APP_TITLE = "🤖 AI Resume Screening & Job Market Analytics"


# =========================================================
# LOAD DATASETS
# =========================================================

@st.cache_data
def load_data():

    data = {}

    try:
        data["resume"] = pd.read_csv("resume_data.csv")
    except Exception:
        data["resume"] = pd.DataFrame()

    try:
        data["salary"] = pd.read_csv("ds_salaries.csv")
    except Exception:
        data["salary"] = pd.DataFrame()

    try:
        data["jobs"] = pd.read_csv(
            "DataAnalyst.csv.zip",
            compression="zip"
        )
    except Exception:
        data["jobs"] = pd.DataFrame()

    try:
        data["people"] = pd.read_csv("01_people.csv")
    except Exception:
        data["people"] = pd.DataFrame()

    return data


data = load_data()

resume_df = data["resume"]
salary_df = data["salary"]
jobs_df = data["jobs"]
people_df = data["people"]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Select Section",
    [
        "🏠 Home",
        "📊 EDA",
        "📄 ATS Score",
        "🧠 Skill Gap",
        "💼 Job Recommendation",
        "📈 Salary Analytics",
        "💰 Salary Prediction",
        "ℹ️ About"
    ]
)


# =========================================================
# DATASET STATUS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Dataset Status")

if not resume_df.empty:
    st.sidebar.success("✅ Resume dataset loaded")
else:
    st.sidebar.warning("⚠️ Resume dataset unavailable")

if not salary_df.empty:
    st.sidebar.success("✅ Salary dataset loaded")
else:
    st.sidebar.warning("⚠️ Salary dataset unavailable")

if not jobs_df.empty:
    st.sidebar.success("✅ Job dataset loaded")
else:
    st.sidebar.warning("⚠️ Job dataset unavailable")

if not people_df.empty:
    st.sidebar.success("✅ People dataset loaded")
else:
    st.sidebar.warning("⚠️ People dataset unavailable")


# =========================================================
# SESSION STATE
# =========================================================

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

if "resume_skills" not in st.session_state:
    st.session_state["resume_skills"] = []

if "ats_score" not in st.session_state:
    st.session_state["ats_score"] = 0


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.title(APP_TITLE)

    st.write(
        "An AI-powered platform for resume analysis, "
        "skill assessment, job recommendation and salary analytics."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Resume Analysis",
        "PDF + DOCX"
    )

    col2.metric(
        "🎯 ATS Analysis",
        "Skill Matching"
    )

    col3.metric(
        "💼 Job Recommendation",
        "AI Matching"
    )

    col4.metric(
        "💰 Salary Analytics",
        "INR"
    )

    st.markdown("---")

    st.subheader("🚀 Project Modules")

    modules = [
        ("📊 EDA", "Explore job-market and salary trends."),
        ("📄 ATS Score", "Analyze resume compatibility with target skills."),
        ("🧠 Skill Gap", "Identify missing skills."),
        ("💼 Job Recommendation", "Recommend relevant jobs based on skills."),
        ("📈 Salary Analytics", "Analyze salary trends and distributions."),
        ("💰 Salary Prediction", "Estimate salary using job-related information.")
    ]

    for title, description in modules:
        st.markdown(f"### {title}")
        st.write(description)


# =========================================================
# EDA
# =========================================================

elif menu == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")

    if salary_df.empty:
        st.error("Salary dataset is not available.")
        st.stop()

    st.write(
        "Explore salary, experience, employment and job-market trends."
    )

    df = salary_df.copy()

    if "salary_in_usd" in df.columns:

        USD_TO_INR = 87

        df["salary_in_inr"] = (
            df["salary_in_usd"] * USD_TO_INR
        )

    st.subheader("📌 Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Records", len(df))

    if "job_title" in df.columns:
        c2.metric(
            "Job Titles",
            df["job_title"].nunique()
        )

    if "company_location" in df.columns:
        c3.metric(
            "Countries",
            df["company_location"].nunique()
        )

    if "salary_in_inr" in df.columns:
        c4.metric(
            "Average Salary",
            f"₹{df['salary_in_inr'].mean():,.0f}"
        )

    st.markdown("---")

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )


# =========================================================
# ATS SCORE
# =========================================================

elif menu == "📄 ATS Score":

    st.title("📄 ATS Resume Score")

    st.info(
        "Upload your resume in PDF or DOCX format to analyze "
        "skills and calculate an ATS compatibility score."
    )

    uploaded_file = st.file_uploader(
        "📂 Upload Resume",
        type=["pdf", "docx"]
    )

    if uploaded_file is None:

        st.warning("Please upload your resume.")

    else:

        st.success("✅ Resume uploaded successfully!")

        resume_text = ""

        if uploaded_file.type == "application/pdf":

            with pdfplumber.open(uploaded_file) as pdf:

                for page in pdf.pages:

                    text = page.extract_text()

                    if text:
                        resume_text += text + " "

        else:

            doc = Document(uploaded_file)

            for paragraph in doc.paragraphs:

                resume_text += paragraph.text + " "

        resume_text = resume_text.lower()

        st.session_state["resume_text"] = resume_text

        st.success("✅ Resume text extracted successfully.")

        st.write(
            f"Characters extracted: {len(resume_text)}"
        )


# =========================================================
# SKILL GAP
# =========================================================

elif menu == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analysis")

    if not st.session_state["resume_skills"]:

        st.info(
            "Please analyze your resume from the ATS Score section first."
        )

    else:

        st.write(
            "Your detected skills will be compared with target skills."
        )


# =========================================================
# JOB RECOMMENDATION
# =========================================================

elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    st.info(
        "Job recommendations will be generated based on "
        "the skills detected from your resume."
    )


# =========================================================
# SALARY ANALYTICS
# =========================================================

elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics")

    if salary_df.empty:

        st.error("Salary dataset is unavailable.")

    else:

        df = salary_df.copy()

        if "salary_in_usd" in df.columns:

            df["salary_in_inr"] = (
                df["salary_in_usd"] * 87
            )

            st.metric(
                "Average Salary",
                f"₹{df['salary_in_inr'].mean():,.0f}"
            )


# =========================================================
# SALARY PREDICTION
# =========================================================

elif menu == "💰 Salary Prediction":

    st.title("💰 Salary Prediction")

    st.info(
        "Salary prediction module will estimate expected "
        "annual salary based on job-related features."
    )


# =========================================================
# ABOUT
# =========================================================

elif menu == "ℹ️ About":

    st.title("ℹ️ About This Project")

    st.write(
        "AI Resume Screening & Job Market Analytics is a "
        "Data Analytics and AI-based project designed to help "
        "students and job seekers understand their resume "
        "strengths, skill gaps, job opportunities and salary trends."
    )

    st.markdown("### 🛠 Technologies")

    st.write(
        "Python • Streamlit • Pandas • NumPy • Plotly • "
        "Scikit-learn • PDFPlumber • Python-DOCX"
    )
