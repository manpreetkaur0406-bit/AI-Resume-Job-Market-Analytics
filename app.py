# ============================================================
# 🤖 AI RESUME SCREENING & JOB MARKET ANALYTICS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import pdfplumber
import re

from docx import Document


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

APP_TITLE = "🤖 AI Resume Screening & Job Market Analytics"

# Dataset salary is in USD.
# We display salary in Indian Rupees.
USD_TO_INR = 87


# ============================================================
# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

if "resume_skills" not in st.session_state:
    st.session_state["resume_skills"] = []

if "resume_profile" not in st.session_state:
    st.session_state["resume_profile"] = {}

if "ats_score" not in st.session_state:
    st.session_state["ats_score"] = 0


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_DATABASE = [

    # Programming
    "python",
    "r",
    "java",
    "c",
    "c++",

    # Data Analytics
    "sql",
    "excel",
    "power bi",
    "tableau",
    "statistics",
    "data analysis",
    "data analytics",

    # Data Science / AI
    "data science",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",

    # Cloud
    "aws",
    "azure",
    "google cloud",

    # Development / Tools
    "git",
    "github",
    "docker",
    "linux",

    # Soft Skills
    "communication",
    "teamwork",
    "problem solving",
    "critical thinking",
    "leadership"
]


# ============================================================
# DEFAULT ATS SKILLS
# ============================================================

DEFAULT_REQUIRED_SKILLS = [

    "python",
    "sql",
    "excel",
    "power bi",
    "statistics",
    "pandas",
    "machine learning",
    "git"

]


# ============================================================
# DATASET LOADING
# ============================================================

@st.cache_data
def load_resume_data():

    try:
        return pd.read_csv("resume_data.csv")

    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_salary_data():

    try:
        return pd.read_csv("ds_salaries.csv")

    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_job_data():

    try:
        return pd.read_csv(
            "DataAnalyst.csv.zip",
            compression="zip"
        )

    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_people_data():

    try:
        return pd.read_csv("01_people.csv")

    except Exception:
        return pd.DataFrame()


# ============================================================
# LOAD DATASETS
# ============================================================

resume_df = load_resume_data()

salary_df = load_salary_data()

jobs_df = load_job_data()

people_df = load_people_data()


# ============================================================
# PREPARE SALARY DATA
# ============================================================

if not salary_df.empty:

    salary_df = salary_df.copy()

    # Remove unwanted index column
    salary_df = salary_df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )

    # Convert USD → INR
    if "salary_in_usd" in salary_df.columns:

        salary_df["salary_in_inr"] = (
            salary_df["salary_in_usd"] * USD_TO_INR
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 AI Career Analytics")

st.sidebar.caption(
    "Resume Screening • Job Recommendation • Salary Analytics"
)

st.sidebar.markdown("---")


# ============================================================
# DATASET STATUS
# ============================================================

st.sidebar.subheader("📂 Dataset Status")


if not resume_df.empty:

    st.sidebar.success("✅ Resume dataset")

else:

    st.sidebar.warning("⚠️ Resume dataset not found")


if not salary_df.empty:

    st.sidebar.success("✅ Salary dataset")

else:

    st.sidebar.warning("⚠️ Salary dataset not found")


if not jobs_df.empty:

    st.sidebar.success("✅ Job dataset")

else:

    st.sidebar.warning("⚠️ Job dataset not found")


if not people_df.empty:

    st.sidebar.success("✅ People dataset")

else:

    st.sidebar.warning("⚠️ People dataset not found")


st.sidebar.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

menu = st.sidebar.radio(

    "📌 Navigation",

    [

        "🏠 Home",

        "📊 EDA",

        "📄 ATS Score",

        "🧠 Skill Gap",

        "💼 Job Recommendation",

        "📈 Salary Analytics",

        "💰 Salary Prediction",

        "📥 Resume Report",

        "ℹ️ About"

    ]

)


# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.title(APP_TITLE)

    st.subheader(
        "🎯 AI-powered resume analysis and career guidance"
    )

    st.write(
        """
        This application analyzes a candidate's resume,
        identifies relevant skills, evaluates ATS compatibility,
        finds skill gaps, recommends suitable jobs and provides
        salary insights using historical job-market data.
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Project Statistics
    # --------------------------------------------------------

    st.subheader("📊 Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Resume Records",
        len(resume_df)
    )

    col2.metric(
        "💼 Job Records",
        len(jobs_df)
    )

    col3.metric(
        "💰 Salary Records",
        len(salary_df)
    )

    col4.metric(
        "🧠 Skills Tracked",
        len(SKILL_DATABASE)
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Main Features
    # --------------------------------------------------------

    st.subheader("🚀 Main Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 📄 Resume Analysis

            Upload a PDF or DOCX resume and extract:

            - Personal information
            - Education
            - Experience
            - Skills
            - Projects
            - Certifications
            """
        )

    with col2:

        st.markdown(
            """
            ### 🎯 Career Intelligence

            Analyze:

            - ATS compatibility
            - Skill gaps
            - Suitable job roles
            - Job matching
            - Career opportunities
            """
        )

    with col3:

        st.markdown(
            """
            ### 💰 Salary Intelligence

            Explore:

            - Salary trends
            - Experience-based salary
            - Job-wise salary
            - Salary prediction
            - Market analytics

            **All salaries are shown in ₹ INR.**
            """
        )

    st.markdown("---")

    st.info(
        "👈 Select a module from the sidebar to start the analysis."
    )


# ============================================================
# EDA PLACEHOLDER
# ============================================================

elif menu == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")

    st.info(
        "EDA module will be added in Part 3."
    )


# ============================================================
# ATS PLACEHOLDER
# ============================================================

elif menu == "📄 ATS Score":

    st.title("📄 ATS Resume Score")

    st.info(
        "Enhanced ATS Resume Analyzer will be added in Part 5."
    )


# ============================================================
# SKILL GAP PLACEHOLDER
# ============================================================

elif menu == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analysis")

    st.info(
        "Skill Gap Analysis will be added in Part 6."
    )


# ============================================================
# JOB RECOMMENDATION PLACEHOLDER
# ============================================================

elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    st.info(
        "Explainable Job Recommendation will be added in Part 7."
    )


# ============================================================
# SALARY ANALYTICS PLACEHOLDER
# ============================================================

elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics")

    st.info(
        "Enhanced Salary Analytics will be added in Part 9."
    )


# ============================================================
# SALARY PREDICTION PLACEHOLDER
# ============================================================

elif menu == "💰 Salary Prediction":

    st.title("💰 Salary Prediction")

    st.info(
        "ML-based Salary Prediction will be added in Part 8."
    )


# ============================================================
# RESUME REPORT PLACEHOLDER
# ============================================================

elif menu == "📥 Resume Report":

    st.title("📥 Resume Analysis Report")

    st.info(
        "Downloadable Resume Report will be added in Part 10."
    )


# ============================================================
# ABOUT
# ============================================================

elif menu == "ℹ️ About":

    st.title("ℹ️ About the Project")

    st.markdown(
        """
        ## 🤖 AI Resume Screening & Job Market Analytics

        A final-year Data Analytics project that combines
        resume analysis, ATS evaluation, skill-gap detection,
        job recommendation and salary analytics.

        ### Technologies

        - Python
        - Streamlit
        - Pandas
        - NumPy
        - Plotly
        - Scikit-learn
        - PDFPlumber
        - python-docx

        ### Currency

        Salary information is displayed in:

        **🇮🇳 Indian Rupees (₹ INR)**

        ### Project Goal

        The goal is to help students understand their resume,
        identify missing skills, discover suitable job roles
        and understand salary trends.
        """
    )
