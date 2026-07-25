import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import re
import pdfplumber

from docx import Document

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Resume  & Job Analytics",
    page_icon="🤖",
    layout="wide"
)



# ================= LOAD DATA =================


@st.cache_data
def load_csv(file):

    try:
        return pd.read_csv(file)

    except:

        return pd.DataFrame()



resume_df = load_csv(
    "resume_data.csv"
)

salary_df = load_csv(
    "ds_salaries.csv"
)



try:

    jobs_df = pd.read_csv(
        "DataAnalyst.csv.zip",
        compression="zip"
    )

except:

    jobs_df = pd.DataFrame()



# ================= MODEL =================


@st.cache_resource
def load_model():

    try:

        return joblib.load(
            "salary_prediction_model.pkl"
        )

    except:

        return None



model = load_model()



# ================= TEXT FUNCTIONS =================


def clean_text(text):

    text = str(text).lower()

    text = re.sub(
        "[^a-z ]",
        " ",
        text
    )

    return text



def extract_text(file):

    text=""


    if file.name.endswith(".pdf"):

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                text += page.extract_text() or ""



    elif file.name.endswith(".docx"):

        doc = Document(file)

        for para in doc.paragraphs:

            text += para.text


    return text



# ================= ATS SCORE =================


def calculate_ats(resume,job):


    vectorizer = TfidfVectorizer()


    vectors = vectorizer.fit_transform(
        [
            clean_text(resume),
            clean_text(job)
        ]
    )


    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]


    return round(score*100,2)




# ================= SKILLS =================


skills_list=[

"python",
"sql",
"machine learning",
"data science",
"statistics",
"excel",
"power bi",
"tableau",
"aws",
"git",
"nlp",
"deep learning"

]



def extract_skills(text):

    text=text.lower()

    found=[]


    for skill in skills_list:

        if skill in text:

            found.append(skill)


    return found




# ================= JOB RECOMMENDATION =================


def recommend_jobs(resume):


    if jobs_df.empty:

        return pd.DataFrame()


    descriptions = jobs_df[
        "Job Description"
    ].astype(str).tolist()



    vectorizer=TfidfVectorizer()


    matrix=vectorizer.fit_transform(
        [resume]+descriptions
    )


    similarity=cosine_similarity(
        matrix[0],
        matrix[1:]
    )[0]


    result=jobs_df.copy()


    result["Match Score"]=(similarity*100).round(2)


    return result.sort_values(
        "Match Score",
        ascending=False
    ).head(10)




# ================= SIDEBAR =================


menu=st.sidebar.radio(

"Navigation",

[
"🏠 Home",
"📊 EDA Dashboard",
"📄 ATS Resume Checker",
"🧠 Skill Gap Analysis",
"💼 Job Recommendation",
"📈 Salary Analytics",
"💰 Salary Prediction",
"ℹ️ About"
]

)



# ================= HOME =================


if menu=="🏠 Home":


    st.title(
        "🤖 AI Resume Screening & Job Market Analytics"
    )


    st.markdown(
    """

    ### Smart Career Analytics Platform


    Features:

    ✅ Resume ATS Score

    ✅ Skill Gap Detection

    ✅ AI Job Recommendation

    ✅ Salary Analysis

    ✅ Salary Prediction


    Built using Data Analytics + Machine Learning


    """
    )



    col1,col2,col3=st.columns(3)


    col1.metric(
        "Resume Dataset",
        len(resume_df)
    )


    col2.metric(
        "Jobs Available",
        len(jobs_df)
    )


    col3.metric(
        "Salary Records",
        len(salary_df)
    )





# ================= EDA =================


elif menu=="📊 EDA Dashboard":


    st.title(
        "📊 Exploratory Data Analysis"
    )


    if salary_df.empty:

        st.warning(
            "Salary dataset missing"
        )

    else:


        st.subheader(
            "Salary Dataset"
        )


        st.dataframe(
            salary_df.head()
        )


        fig=px.histogram(

            salary_df,

            x="salary_in_usd",

            title="Salary Distribution"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )




# ================= ATS =================


elif menu=="📄 ATS Resume Checker":


    st.title(
        "📄 AI ATS Resume Score"
    )


    uploaded=st.file_uploader(

        "Upload Resume",

        type=["pdf","docx"]

    )


    job_description=st.text_area(

        "Paste Job Description"

    )



    if uploaded and job_description:


        resume_text=extract_text(
            uploaded
        )


        score=calculate_ats(

            resume_text,

            job_description

        )


        st.metric(
            "ATS Score",
            f"{score}%"
        )


        st.subheader(
            "Matched Skills"
        )


        st.write(
            extract_skills(resume_text)
        )



# ================= SKILL GAP =================


elif menu=="🧠 Skill Gap Analysis":


    st.title(
        "🧠 Skill Gap Analysis"
    )


    resume=st.text_area(
        "Enter Resume Skills"
    )


    required=st.multiselect(

        "Required Skills",

        skills_list

    )



    if st.button("Analyze"):


        user_skills=extract_skills(
            resume
        )


        missing=list(

            set(required)-set(user_skills)

        )


        st.success(
            "Your Skills"
        )

        st.write(user_skills)


        st.error(
            "Missing Skills"
        )

        st.write(missing)





# ================= JOB =================


elif menu=="💼 Job Recommendation":


    st.title(
        "💼 AI Job Recommendation"
    )


    resume=st.text_area(
        "Enter Resume"
    )


    if st.button(
        "Find Jobs"
    ):


        result=recommend_jobs(
            resume
        )


        st.dataframe(
            result
        )





# ================= SALARY =================


elif menu=="📈 Salary Analytics":


    st.title(
        "📈 Salary Market Analysis"
    )


    if not salary_df.empty:


        exp=salary_df.groupby(
            "experience_level"
        )[
            "salary_in_usd"
        ].mean().reset_index()



        fig=px.bar(

            exp,

            x="experience_level",

            y="salary_in_usd",

            title="Average Salary"

        )


        st.plotly_chart(
            fig
        )



# ================= PREDICTION =================


elif menu=="💰 Salary Prediction":


    st.title(
        "💰 Salary Prediction"
    )


    if model is None:

        st.error(
            "Model file missing"
        )


    else:


        experience=st.number_input(
            "Experience Level",
            0,4
        )


        remote=st.number_input(
            "Remote Ratio",
            0,100
        )


        company=st.number_input(
            "Company Size",
            0,2
        )


        if st.button(
            "Predict"
        ):


            data=pd.DataFrame(

            [[
            2025,
            experience,
            0,
            10,
            0,
            20,
            remote,
            20,
            company
            ]],

            columns=[
            "work_year",
            "experience_level",
            "employment_type",
            "job_title",
            "salary_currency",
            "employee_residence",
            "remote_ratio",
            "company_location",
            "company_size"
            ]

            )


            prediction=model.predict(data)


            st.success(

            f"Predicted Salary: ${prediction[0]:,.0f}"

            )





# ================= ABOUT =================


elif menu=="ℹ️ About":


    st.title(
        "ℹ️ About Project"
    )


    st.write(
    """

    ## AI Resume Screening & Job Market Analytics


    Technologies:

    - Python
    - Streamlit
    - Pandas
    - Machine Learning
    - NLP
    - Plotly


    Objective:

    To build an intelligent platform that helps
    candidates analyze resumes, find suitable jobs,
    understand market salaries and improve skills.


    """
    )
