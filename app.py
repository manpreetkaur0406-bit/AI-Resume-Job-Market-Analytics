# ============================================================
# 🤖 AI RESUME SCREENING & JOB MARKET ANALYTICS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib
import pdfplumber
import re

from docx import Document


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening & Job Market Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

# Currency conversion used for displaying salary data.
# Dataset salary is in USD.
USD_TO_INR = 87


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

    # Data Analysis
    "sql",
    "excel",
    "power bi",
    "tableau",
    "statistics",
    "data analysis",
    "data analytics",

    # Data Science
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

    # Tools
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
# REQUIRED SKILLS FOR DEFAULT ATS ANALYSIS
# ============================================================

DEFAULT_REQUIRED_SKILLS = [

    "python",
    "sql",
    "excel",
    "power bi",
    "machine learning",
    "statistics",
    "git",
    "pandas"

]


# ============================================================
# DATASET LOADING FUNCTION
# ============================================================

@st.cache_data
def load_datasets():

    datasets = {}

    # Resume Dataset
    try:
        datasets["resume"] = pd.read_csv("resume_data.csv")
    except Exception:
        datasets["resume"] = pd.DataFrame()

    # Salary Dataset
    try:
        datasets["salary"] = pd.read_csv("ds_salaries.csv")
    except Exception:
        datasets["salary"] = pd.DataFrame()

    # Job Dataset
    try:
        datasets["jobs"] = pd.read_csv(
            "DataAnalyst.csv.zip",
            compression="zip"
        )
    except Exception:
        datasets["jobs"] = pd.DataFrame()

    # People Dataset
    try:
        datasets["people"] = pd.read_csv("01_people.csv")
    except Exception:
        datasets["people"] = pd.DataFrame()

    return datasets


# ============================================================
# LOAD ALL DATASETS
# ============================================================

data = load_datasets()

resume_df = data["resume"]
salary_df = data["salary"]
jobs_df = data["jobs"]
people_df = data["people"]


# ============================================================
# SALARY DATA PREPARATION
# ============================================================

if not salary_df.empty:

    salary_df = salary_df.copy()

    # Remove unwanted index column if present
    salary_df = salary_df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )

    # Convert salary from USD to INR
    if "salary_in_usd" in salary_df.columns:

        salary_df["salary_inr"] = (
            salary_df["salary_in_usd"] * USD_TO_INR
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 AI Career Analytics")

st.sidebar.markdown(
    "### 📌 Project Navigation"
)


# Dataset status

if not resume_df.empty:
    st.sidebar.success("✅ Resume dataset loaded")
else:
    st.sidebar.warning("⚠ Resume dataset unavailable")


if not salary_df.empty:
    st.sidebar.success("✅ Salary dataset loaded")
else:
    st.sidebar.warning("⚠ Salary dataset unavailable")


if not jobs_df.empty:
    st.sidebar.success("✅ Job dataset loaded")
else:
    st.sidebar.warning("⚠ Job dataset unavailable")


if not people_df.empty:
    st.sidebar.success("✅ People dataset loaded")
else:
    st.sidebar.warning("⚠ People dataset unavailable")


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
        "ℹ️ About"
    ]
)
