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

st.set_page_config(
    page_title="AI Resume Screening & Job Market Analytics",
    page_icon="🤖",
    layout="wide"
)


menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "📊 EDA",
        "📄 ATS Score",
        "💼 Job Recommendation",
        "📈 Salary Analytics",
        "💰 Salary Prediction",
        "ℹ️ About"
    ]
)
if menu == "🏠 Home":

    st.title("🤖 AI Resume Screening & Job Market Analytics")

    st.markdown("""
    Welcome to the **AI Resume Screening & Job Market Analytics** platform.

    This application helps job seekers analyze their resumes, improve ATS scores,
    discover suitable job opportunities, predict salaries, and explore current
    job market trends using Artificial Intelligence and Data Analytics.
    """)

    st.markdown("---")

    # ===========================
    # Dashboard Metrics
    # ===========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Resume Support",
            "PDF & DOCX"
        )

    with col2:
        st.metric(
            "💼 Job Roles",
            "1000+"
        )

    with col3:
        st.metric(
            "📈 Salary Dataset",
            "600+ Records"
        )

    with col4:
        st.metric(
            "🤖 AI Features",
            "7 Modules"
        )

    st.markdown("---")
    st.dataframe(jobs_df.head())

elif menu == "📊 EDA":

    st.title("📊 Exploratory Data Analysis Dashboard")

    st.write(
        "Analyze salary trends, job roles, experience levels and employment insights."
    )

    # =====================================
    # Convert Salary to INR
    # =====================================

    df = salary_df.copy()

    USD_TO_INR = 87

    df["salary_in_inr"] = df["salary_in_usd"] * USD_TO_INR

    # =====================================
    # Dashboard KPIs
    # =====================================

    total_records = len(df)
    total_jobs = df["job_title"].nunique()
    total_countries = df["company_location"].nunique()
    total_companies = df["company_size"].count()

    avg_salary = int(df["salary_in_inr"].mean())
    median_salary = int(df["salary_in_inr"].median())
    highest_salary = int(df["salary_in_inr"].max())
    lowest_salary = int(df["salary_in_inr"].min())

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Total Records", total_records)
    c2.metric("💼 Job Titles", total_jobs)
    c3.metric("🌍 Countries", total_countries)
    c4.metric("🏢 Companies", total_companies)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Average Salary", f"₹{avg_salary:,.0f}")
    c2.metric("📊 Median Salary", f"₹{median_salary:,.0f}")
    c3.metric("🚀 Highest Salary", f"₹{highest_salary:,.0f}")
    c4.metric("📉 Lowest Salary", f"₹{lowest_salary:,.0f}")

    st.markdown("---")

    # =====================================
    # Filters
    # =====================================

    st.subheader("🎛️ Dataset Filters")

    col1, col2, col3 = st.columns(3)

    experience = col1.selectbox(
        "Experience Level",
        ["All"] + sorted(df["experience_level"].unique())
    )

    employment = col2.selectbox(
        "Employment Type",
        ["All"] + sorted(df["employment_type"].unique())
    )

    company_size = col3.selectbox(
        "Company Size",
        ["All"] + sorted(df["company_size"].unique())
    )

    col4, col5, col6 = st.columns(3)

    remote = col4.selectbox(
        "Remote Ratio",
        ["All"] + sorted(df["remote_ratio"].astype(str).unique())
    )

    work_year = col5.selectbox(
        "Work Year",
        ["All"] + sorted(df["work_year"].astype(str).unique())
    )

    country = col6.selectbox(
        "Country",
        ["All"] + sorted(df["company_location"].unique())
    )

    # =====================================
    # Apply Filters
    # =====================================

    filtered_df = df.copy()

    if experience != "All":
        filtered_df = filtered_df[
            filtered_df["experience_level"] == experience
        ]

    if employment != "All":
        filtered_df = filtered_df[
            filtered_df["employment_type"] == employment
        ]

    if company_size != "All":
        filtered_df = filtered_df[
            filtered_df["company_size"] == company_size
        ]

    if remote != "All":
        filtered_df = filtered_df[
            filtered_df["remote_ratio"].astype(str) == remote
        ]

    if work_year != "All":
        filtered_df = filtered_df[
            filtered_df["work_year"].astype(str) == work_year
        ]

    if country != "All":
        filtered_df = filtered_df[
            filtered_df["company_location"] == country
        ]

    st.success(f"Showing {len(filtered_df)} records")

    st.markdown("---")

    # =====================================
    # Search Job Title
    # =====================================

    search = st.text_input(
        "🔍 Search Job Title"
    )

    if search:

        filtered_df = filtered_df[
            filtered_df["job_title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # =====================================
    # Dataset Preview
    # =====================================

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # Download Dataset
    # =====================================

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv,
        file_name="filtered_salary_dataset.csv",
        mime="text/csv"
    )

    st.markdown("---")
    # =====================================
    # 📊 Salary Distribution
    # =====================================

    st.subheader("📊 Salary Distribution (INR)")

    fig = px.histogram(
        filtered_df,
        x="salary_in_inr",
        nbins=30,
        title="Salary Distribution",
        color_discrete_sequence=["#4F46E5"]
    )

    fig.update_layout(
        xaxis_title="Salary (₹)",
        yaxis_title="Number of Employees"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        f"Average Salary: ₹{filtered_df['salary_in_inr'].mean():,.0f}"
    )

    st.markdown("---")

    # =====================================
    # 📈 Salary by Experience
    # =====================================

    st.subheader("📈 Average Salary by Experience Level")

    exp_salary = (
        filtered_df
        .groupby("experience_level")["salary_in_inr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        exp_salary,
        x="experience_level",
        y="salary_in_inr",
        color="experience_level",
        title="Salary by Experience Level"
    )

    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 💼 Top 10 Highest Paying Jobs
    # =====================================

    st.subheader("💼 Top 10 Highest Paying Job Roles")

    top_jobs = (
        filtered_df
        .groupby("job_title")["salary_in_inr"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_jobs,
        x="salary_in_inr",
        y="job_title",
        orientation="h",
        color="salary_in_inr",
        title="Top 10 Highest Paying Jobs"
    )

    fig.update_layout(
        xaxis_title="Average Salary (₹)",
        yaxis_title="Job Role"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 🌍 Salary by Country
    # =====================================

    st.subheader("🌍 Top Countries by Average Salary")

    country_salary = (
        filtered_df
        .groupby("company_location")["salary_in_inr"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        country_salary,
        x="company_location",
        y="salary_in_inr",
        color="salary_in_inr",
        title="Average Salary by Country"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 🏠 Remote Work Distribution
    # =====================================

    st.subheader("🏠 Remote Work Distribution")

    remote_df = (
        filtered_df["remote_ratio"]
        .value_counts()
        .reset_index()
    )

    remote_df.columns = ["Remote Ratio", "Count"]

    fig = px.pie(
        remote_df,
        names="Remote Ratio",
        values="Count",
        title="Remote Work Ratio"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 🏢 Company Size Distribution
    # =====================================

    st.subheader("🏢 Company Size Distribution")

    company_df = (
        filtered_df["company_size"]
        .value_counts()
        .reset_index()
    )

    company_df.columns = ["Company Size", "Count"]

    fig = px.bar(
        company_df,
        x="Company Size",
        y="Count",
        color="Company Size",
        title="Company Size"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 💼 Employment Type
    # =====================================

    st.subheader("💼 Employment Type Distribution")

    employment_df = (
        filtered_df["employment_type"]
        .value_counts()
        .reset_index()
    )

    employment_df.columns = ["Employment Type", "Count"]

    fig = px.pie(
        employment_df,
        names="Employment Type",
        values="Count",
        title="Employment Type Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =====================================
    # 📅 Salary Trend by Work Year
    # =====================================

    st.subheader("📅 Salary Trend")

    trend = (
        filtered_df
        .groupby("work_year")["salary_in_inr"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="work_year",
        y="salary_in_inr",
        markers=True,
        title="Average Salary Trend"
    )

    fig.update_layout(
        xaxis_title="Work Year",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    

elif menu == "📄 ATS Score":

    st.title("📄 ATS Resume Score")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

    # No resume uploaded
    if uploaded_file is None:

        st.info("📂 Please upload your resume in PDF or DOCX format.")

        st.stop()

    # Invalid file
    if uploaded_file.type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:

        st.error("❌ Only PDF and DOCX files are supported.")
        st.session_state["resume_skills"]
        st.stop()

    st.success("✅ Resume uploaded successfully!")

    # ==========================
    # Extract Resume Text
    # ==========================

    resume_text = ""

    if uploaded_file.type == "application/pdf":

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    resume_text += text.lower() + " "

    else:

        doc = Document(uploaded_file)

        for para in doc.paragraphs:

            resume_text += para.text.lower() + " "

    # ==========================
    # Skill Database
    # ==========================

    skill_database = [

    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "deep learning",
    "statistics",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",
    "aws",
    "azure",
    "git",
    "github",
    "docker",
    "linux",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "r",
    "spark",
    "hadoop",
    "flask",
    "streamlit",
    "opencv",
    "nlp",
    "computer vision",
    "matplotlib",
    "plotly"

]

    # ==========================
    # Extract Skills
    # ==========================

    resume_skills = []

    for skill in skill_database:

        if skill in resume_text:

            resume_skills.append(skill)

    resume_skills = sorted(list(set(resume_skills)))

    st.session_state["resume_skills"] = resume_skills

    # ==========================
    # Required Skills
    # ==========================

    required_skills = [

    "python",
    "sql",
    "excel",
    "power bi",
    "machine learning",
    "statistics",
    "git",
    "pandas"

]
   
    matched_skills = list(
        set(resume_skills) &
        set(required_skills)
    )

    missing_skills = list(
        set(required_skills) -
        set(resume_skills)
    )

    ats_score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    # ==========================
    # ATS Score
    # ==========================

    st.subheader("📊 ATS Score")

    st.metric(
        "Score",
        f"{ats_score:.0f}%"
    )

    st.progress(int(ats_score))

    # ==========================
    # Skills Found
    # ==========================

    st.subheader("✅ Skills Found")

    if resume_skills:
        st.write(", ".join(resume_skills))
    else:
        st.warning("No technical skills found in the uploaded resume.")
    # ==========================
    # Matched Skills
    # ==========================

    st.subheader("🎯 Matched Skills")

    if matched_skills:

        for skill in matched_skills:

            st.success(skill.title())

    else:

        st.warning("No matching skills found.")

    # ==========================
    # Missing Skills
    # ==========================

    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            st.error(skill.title())

    else:

        st.success("Excellent! Your resume contains all required skills.")

    # ==========================
    # ATS Feedback
    # ==========================

    st.subheader("💡 ATS Feedback")

    if ats_score >= 80:

        st.success("Excellent resume! Your profile matches most of the required skills.")

    elif ats_score >= 60:

        st.info("Good resume. Adding the missing skills can improve your ATS score.")

    elif ats_score >= 40:

        st.warning("Average ATS score. Consider improving your technical skills and resume.")

    else:

        st.error("Low ATS score. Add more relevant technical skills to improve your chances.")


elif menu == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analysis")
    
elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    # Check if resume has been uploaded
    if "resume_skills" not in st.session_state:

        st.warning("📄 Please upload your resume first from the ATS Score page.")

    else:

        candidate_skills = st.session_state["resume_skills"]

        # Remove duplicate skills
        candidate_skills = list(set(candidate_skills))

        st.subheader("✅ Resume Skills")

        if len(candidate_skills) == 0:

            st.error("❌ No technical skills found in your resume.")
            st.stop()

        st.write(", ".join(candidate_skills))

        recommendations = []

        # Calculate Match Score
        for _, row in jobs_df.iterrows():

            description = str(row["Job Description"]).lower()

            score = 0

            for skill in candidate_skills:

                if skill.lower() in description:
                    score += 1

            recommendations.append(score)

        jobs_df["Match Score"] = recommendations

        # Keep only jobs with at least 2 matched skills
        top_jobs = jobs_df[jobs_df["Match Score"] >= 2]

        if top_jobs.empty:

            st.error("❌ No jobs recommended for your resume.")

        else:

            top_jobs = top_jobs.sort_values(
                by="Match Score",
                ascending=False
            ).head(10)

            st.success(f"🎯 {len(top_jobs)} Matching Jobs Found")

            for _, row in top_jobs.iterrows():

                match_percent = int(
                    (row["Match Score"] / len(candidate_skills)) * 100
                )

                if match_percent > 100:
                    match_percent = 100

                st.markdown("---")

                st.subheader(f"💼 {row['Job Title']}")

                st.write(f"🏢 Company : {row['Company Name']}")
                st.write(f"📍 Location : {row['Location']}")

                st.progress(match_percent)

                st.write(f"⭐ Match Score : {match_percent}%")

                with st.expander("📄 View Job Description"):
                    st.write(row["Job Description"])
                    

    
elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics Dashboard")
    st.write("Explore salary trends in the Data Science job market.")

    # Remove unwanted column
    salary_df = salary_df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Convert USD to INR
    USD_TO_INR = 87
    salary_df["salary_inr"] = salary_df["salary_in_usd"] * USD_TO_INR

    st.markdown("---")

    # ==============================
    # KPI Cards
    # ==============================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Average Salary",
            f"₹ {salary_df['salary_inr'].mean():,.0f}"
        )

    with col2:
        st.metric(
            "📈 Highest Salary",
            f"₹ {salary_df['salary_inr'].max():,.0f}"
        )

    with col3:
        st.metric(
            "📉 Lowest Salary",
            f"₹ {salary_df['salary_inr'].min():,.0f}"
        )

    with col4:
        st.metric(
            "🌍 Countries",
            salary_df["company_location"].nunique()
        )

    st.markdown("---")

    # ==============================
    # Dataset Preview
    # ==============================

    st.subheader("📄 Salary Dataset Preview")
    st.dataframe(salary_df.head())

    # ==============================
    # Average Salary by Experience
    # ==============================

    st.subheader("💼 Average Salary by Experience Level")

    avg_salary = (
        salary_df.groupby("experience_level")["salary_inr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        avg_salary,
        x="experience_level",
        y="salary_inr",
        color="salary_inr",
        text_auto=".2s",
        title="Average Salary by Experience Level"
    )

    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Salary Distribution
    # ==============================

    st.subheader("📊 Salary Distribution")

    fig = px.histogram(
        salary_df,
        x="salary_inr",
        nbins=30,
        title="Salary Distribution"
    )

    fig.update_layout(
        xaxis_title="Salary (₹)",
        yaxis_title="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Top 10 Highest Paying Jobs
    # ==============================

    st.subheader("🏆 Top 10 Highest Paying Job Titles")

    top_jobs = (
        salary_df.groupby("job_title")["salary_inr"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_jobs,
        x="salary_inr",
        y="job_title",
        orientation="h",
        color="salary_inr",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Average Salary (₹)",
        yaxis_title="Job Title"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Top Hiring Countries
    # ==============================

    st.subheader("🌍 Top Hiring Countries")

    countries = (
        salary_df["company_location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    countries.columns = ["Country", "Jobs"]

    fig = px.bar(
        countries,
        x="Country",
        y="Jobs",
        color="Jobs",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Remote Work Distribution
    # ==============================

    st.subheader("🏠 Remote Work Distribution")

    remote = (
        salary_df["remote_ratio"]
        .value_counts()
        .reset_index()
    )

    remote.columns = ["Remote Ratio", "Count"]

    fig = px.pie(
        remote,
        names="Remote Ratio",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Company Size Distribution
    # ==============================

    st.subheader("🏢 Company Size Distribution")

    company = (
        salary_df["company_size"]
        .value_counts()
        .reset_index()
    )

    company.columns = ["Company Size", "Count"]

    fig = px.pie(
        company,
        names="Company Size",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Employment Type
    # ==============================

    st.subheader("📋 Employment Type")

    employment = (
        salary_df["employment_type"]
        .value_counts()
        .reset_index()
    )

    employment.columns = ["Employment Type", "Count"]

    fig = px.bar(
        employment,
        x="Employment Type",
        y="Count",
        color="Count",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Salary by Company Size
    # ==============================

    st.subheader("💵 Average Salary by Company Size")

    company_salary = (
        salary_df.groupby("company_size")["salary_inr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        company_salary,
        x="company_size",
        y="salary_inr",
        color="salary_inr",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Company Size",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)
elif menu == "💰 Salary Prediction":

    st.title("💰 AI Salary Prediction")

    st.write(
        "Estimate your expected annual salary in India based on your job role and experience."
    )

    st.markdown("---")

    # ===============================
    # User Inputs
    # ===============================

    job_role = st.selectbox(
        "💼 Select Job Role",
        [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Engineer",
            "Python Developer",
            "BI Developer"
        ]
    )

    experience = st.slider(
        "👨‍💻 Years of Experience",
        0,
        20,
        0
    )

    st.markdown("---")

    if st.button("💰 Predict Salary"):

        # Base Salaries (Annual INR)

        base_salary = {

            "Data Analyst": 500000,
            "Business Analyst": 600000,
            "Data Scientist": 800000,
            "Machine Learning Engineer": 900000,
            "AI Engineer": 1000000,
            "Data Engineer": 850000,
            "Python Developer": 550000,
            "BI Developer": 650000

        }

        salary = base_salary[job_role]

        # Experience Increment

        if experience == 0:
            salary = salary

        elif experience <= 2:
            salary *= 1.20

        elif experience <= 5:
            salary *= 1.60

        elif experience <= 8:
            salary *= 2.20

        elif experience <= 12:
            salary *= 2.90

        else:
            salary *= 3.60

        salary = int(salary)

        monthly_salary = int(salary / 12)

        lower = int(salary * 0.90)

        upper = int(salary * 1.10)

        st.success("🎉 Salary Prediction Completed")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Annual Salary",
                f"₹ {salary:,.0f}"
            )

        with col2:

            st.metric(
                "Monthly Salary",
                f"₹ {monthly_salary:,.0f}"
            )

        st.progress(100)

        st.info(
            f"📊 Estimated Salary Range : ₹ {lower:,.0f}  -  ₹ {upper:,.0f}"
        )

        st.markdown("---")

        st.subheader("📋 Prediction Summary")

        st.write(f"**Job Role :** {job_role}")

        st.write(f"**Experience :** {experience} Years")

        if experience == 0:

            level = "Fresher"

        elif experience <= 2:

            level = "Junior"

        elif experience <= 5:

            level = "Mid-Level"

        elif experience <= 8:

            level = "Senior"

        else:

            level = "Expert"

        st.write(f"**Experience Level :** {level}")

        st.success(
            "This prediction is based on current Data Science and Analytics salary trends in India."
        )


elif menu == "ℹ️ About":

    st.title("ℹ️ About Project")

    st.write("""
    **AI Resume Screening & Job Market Analytics**

    This project uses Data Analytics and Machine Learning to:

    • Analyze resumes
    • Calculate ATS scores
    • Recommend jobs
    • Analyze salary trends
    • Predict salaries

    **Technologies Used**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Plotly
    
    """)


elif menu == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")

    st.dataframe(resume_df.head())
    st.dataframe(salary_df.head())
    st.dataframe(jobs_df.head())

elif menu == "📄 ATS Score":

    st.title("📄 ATS Resume Score")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

    # No resume uploaded
    if uploaded_file is None:

        st.info("📂 Please upload your resume in PDF or DOCX format.")

        st.stop()

    # Invalid file
    if uploaded_file.type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:

        st.error("❌ Only PDF and DOCX files are supported.")
        st.session_state["resume_skills"]
        st.stop()

    st.success("✅ Resume uploaded successfully!")

    # ==========================
    # Extract Resume Text
    # ==========================

    resume_text = ""

    if uploaded_file.type == "application/pdf":

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    resume_text += text.lower() + " "

    else:

        doc = Document(uploaded_file)

        for para in doc.paragraphs:

            resume_text += para.text.lower() + " "

    # ==========================
    # Skill Database
    # ==========================

    skill_database = [

    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "deep learning",
    "statistics",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",
    "aws",
    "azure",
    "git",
    "github",
    "docker",
    "linux",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "r",
    "spark",
    "hadoop",
    "flask",
    "streamlit",
    "opencv",
    "nlp",
    "computer vision",
    "matplotlib",
    "plotly"

]

    # ==========================
    # Extract Skills
    # ==========================

    resume_skills = []

    for skill in skill_database:

        if skill in resume_text:

            resume_skills.append(skill)

    resume_skills = sorted(list(set(resume_skills)))

    st.session_state["resume_skills"] = resume_skills

    # ==========================
    # Required Skills
    # ==========================

    required_skills = [

    "python",
    "sql",
    "excel",
    "power bi",
    "machine learning",
    "statistics",
    "git",
    "pandas"

]
   
    matched_skills = list(
        set(resume_skills) &
        set(required_skills)
    )

    missing_skills = list(
        set(required_skills) -
        set(resume_skills)
    )

    ats_score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    # ==========================
    # ATS Score
    # ==========================

    st.subheader("📊 ATS Score")

    st.metric(
        "Score",
        f"{ats_score:.0f}%"
    )

    st.progress(int(ats_score))

    # ==========================
    # Skills Found
    # ==========================

    st.subheader("✅ Skills Found")

    if resume_skills:
        st.write(", ".join(resume_skills))
    else:
        st.warning("No technical skills found in the uploaded resume.")
    # ==========================
    # Matched Skills
    # ==========================

    st.subheader("🎯 Matched Skills")

    if matched_skills:

        for skill in matched_skills:

            st.success(skill.title())

    else:

        st.warning("No matching skills found.")

    # ==========================
    # Missing Skills
    # ==========================

    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            st.error(skill.title())

    else:

        st.success("Excellent! Your resume contains all required skills.")

    # ==========================
    # ATS Feedback
    # ==========================

    st.subheader("💡 ATS Feedback")

    if ats_score >= 80:

        st.success("Excellent resume! Your profile matches most of the required skills.")

    elif ats_score >= 60:

        st.info("Good resume. Adding the missing skills can improve your ATS score.")

    elif ats_score >= 40:

        st.warning("Average ATS score. Consider improving your technical skills and resume.")

    else:

        st.error("Low ATS score. Add more relevant technical skills to improve your chances.")


elif menu == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analysis")
    
elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    # Check if resume has been uploaded
    if "resume_skills" not in st.session_state:

        st.warning("📄 Please upload your resume first from the ATS Score page.")

    else:

        candidate_skills = st.session_state["resume_skills"]

        # Remove duplicate skills
        candidate_skills = list(set(candidate_skills))

        st.subheader("✅ Resume Skills")

        if len(candidate_skills) == 0:

            st.error("❌ No technical skills found in your resume.")
            st.stop()

        st.write(", ".join(candidate_skills))

        recommendations = []

        # Calculate Match Score
        for _, row in jobs_df.iterrows():

            description = str(row["Job Description"]).lower()

            score = 0

            for skill in candidate_skills:

                if skill.lower() in description:
                    score += 1

            recommendations.append(score)

        jobs_df["Match Score"] = recommendations

        # Keep only jobs with at least 2 matched skills
        top_jobs = jobs_df[jobs_df["Match Score"] >= 2]

        if top_jobs.empty:

            st.error("❌ No jobs recommended for your resume.")

        else:

            top_jobs = top_jobs.sort_values(
                by="Match Score",
                ascending=False
            ).head(10)

            st.success(f"🎯 {len(top_jobs)} Matching Jobs Found")

            for _, row in top_jobs.iterrows():

                match_percent = int(
                    (row["Match Score"] / len(candidate_skills)) * 100
                )

                if match_percent > 100:
                    match_percent = 100

                st.markdown("---")

                st.subheader(f"💼 {row['Job Title']}")

                st.write(f"🏢 Company : {row['Company Name']}")
                st.write(f"📍 Location : {row['Location']}")

                st.progress(match_percent)

                st.write(f"⭐ Match Score : {match_percent}%")

                with st.expander("📄 View Job Description"):
                    st.write(row["Job Description"])
                    

    
elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics Dashboard")
    st.write("Explore salary trends in the Data Science job market.")

    # Remove unwanted column
    salary_df = salary_df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Convert USD to INR
    USD_TO_INR = 87
    salary_df["salary_inr"] = salary_df["salary_in_usd"] * USD_TO_INR

    st.markdown("---")

    # ==============================
    # KPI Cards
    # ==============================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Average Salary",
            f"₹ {salary_df['salary_inr'].mean():,.0f}"
        )

    with col2:
        st.metric(
            "📈 Highest Salary",
            f"₹ {salary_df['salary_inr'].max():,.0f}"
        )

    with col3:
        st.metric(
            "📉 Lowest Salary",
            f"₹ {salary_df['salary_inr'].min():,.0f}"
        )

    with col4:
        st.metric(
            "🌍 Countries",
            salary_df["company_location"].nunique()
        )

    st.markdown("---")

    # ==============================
    # Dataset Preview
    # ==============================

    st.subheader("📄 Salary Dataset Preview")
    st.dataframe(salary_df.head())

    # ==============================
    # Average Salary by Experience
    # ==============================

    st.subheader("💼 Average Salary by Experience Level")

    avg_salary = (
        salary_df.groupby("experience_level")["salary_inr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        avg_salary,
        x="experience_level",
        y="salary_inr",
        color="salary_inr",
        text_auto=".2s",
        title="Average Salary by Experience Level"
    )

    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Salary Distribution
    # ==============================

    st.subheader("📊 Salary Distribution")

    fig = px.histogram(
        salary_df,
        x="salary_inr",
        nbins=30,
        title="Salary Distribution"
    )

    fig.update_layout(
        xaxis_title="Salary (₹)",
        yaxis_title="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Top 10 Highest Paying Jobs
    # ==============================

    st.subheader("🏆 Top 10 Highest Paying Job Titles")

    top_jobs = (
        salary_df.groupby("job_title")["salary_inr"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_jobs,
        x="salary_inr",
        y="job_title",
        orientation="h",
        color="salary_inr",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Average Salary (₹)",
        yaxis_title="Job Title"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Top Hiring Countries
    # ==============================

    st.subheader("🌍 Top Hiring Countries")

    countries = (
        salary_df["company_location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    countries.columns = ["Country", "Jobs"]

    fig = px.bar(
        countries,
        x="Country",
        y="Jobs",
        color="Jobs",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Remote Work Distribution
    # ==============================

    st.subheader("🏠 Remote Work Distribution")

    remote = (
        salary_df["remote_ratio"]
        .value_counts()
        .reset_index()
    )

    remote.columns = ["Remote Ratio", "Count"]

    fig = px.pie(
        remote,
        names="Remote Ratio",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Company Size Distribution
    # ==============================

    st.subheader("🏢 Company Size Distribution")

    company = (
        salary_df["company_size"]
        .value_counts()
        .reset_index()
    )

    company.columns = ["Company Size", "Count"]

    fig = px.pie(
        company,
        names="Company Size",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Employment Type
    # ==============================

    st.subheader("📋 Employment Type")

    employment = (
        salary_df["employment_type"]
        .value_counts()
        .reset_index()
    )

    employment.columns = ["Employment Type", "Count"]

    fig = px.bar(
        employment,
        x="Employment Type",
        y="Count",
        color="Count",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Salary by Company Size
    # ==============================

    st.subheader("💵 Average Salary by Company Size")

    company_salary = (
        salary_df.groupby("company_size")["salary_inr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        company_salary,
        x="company_size",
        y="salary_inr",
        color="salary_inr",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Company Size",
        yaxis_title="Average Salary (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)
elif menu == "💰 Salary Prediction":

    st.title("💰 AI Salary Prediction")

    st.write(
        "Estimate your expected annual salary in India based on your job role and experience."
    )

    st.markdown("---")

    # ===============================
    # User Inputs
    # ===============================

    job_role = st.selectbox(
        "💼 Select Job Role",
        [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Engineer",
            "Python Developer",
            "BI Developer"
        ]
    )

    experience = st.slider(
        "👨‍💻 Years of Experience",
        0,
        20,
        0
    )

    st.markdown("---")

    if st.button("💰 Predict Salary"):

        # Base Salaries (Annual INR)

        base_salary = {

            "Data Analyst": 500000,
            "Business Analyst": 600000,
            "Data Scientist": 800000,
            "Machine Learning Engineer": 900000,
            "AI Engineer": 1000000,
            "Data Engineer": 850000,
            "Python Developer": 550000,
            "BI Developer": 650000

        }

        salary = base_salary[job_role]

        # Experience Increment

        if experience == 0:
            salary = salary

        elif experience <= 2:
            salary *= 1.20

        elif experience <= 5:
            salary *= 1.60

        elif experience <= 8:
            salary *= 2.20

        elif experience <= 12:
            salary *= 2.90

        else:
            salary *= 3.60

        salary = int(salary)

        monthly_salary = int(salary / 12)

        lower = int(salary * 0.90)

        upper = int(salary * 1.10)

        st.success("🎉 Salary Prediction Completed")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Annual Salary",
                f"₹ {salary:,.0f}"
            )

        with col2:

            st.metric(
                "Monthly Salary",
                f"₹ {monthly_salary:,.0f}"
            )

        st.progress(100)

        st.info(
            f"📊 Estimated Salary Range : ₹ {lower:,.0f}  -  ₹ {upper:,.0f}"
        )

        st.markdown("---")

        st.subheader("📋 Prediction Summary")

        st.write(f"**Job Role :** {job_role}")

        st.write(f"**Experience :** {experience} Years")

        if experience == 0:

            level = "Fresher"

        elif experience <= 2:

            level = "Junior"

        elif experience <= 5:

            level = "Mid-Level"

        elif experience <= 8:

            level = "Senior"

        else:

            level = "Expert"

        st.write(f"**Experience Level :** {level}")

        st.success(
            "This prediction is based on current Data Science and Analytics salary trends in India."
        )


elif menu == "ℹ️ About":

    st.title("ℹ️ About Project")

    st.write("""
    **AI Resume Screening & Job Market Analytics**

    This project uses Data Analytics and Machine Learning to:

    • Analyze resumes
    • Calculate ATS scores
    • Recommend jobs
    • Analyze salary trends
    • Predict salaries

    **Technologies Used**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Plotly
    
    """)







