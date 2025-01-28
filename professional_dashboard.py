import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Professional Profile Dashboard",
    page_icon="👔",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .profile-header {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Mock data - replace with actual API data in production
mock_profile = {
    "name": "Professional Profile Viewer",
    "headline": "Example Professional Dashboard",
    "location": "New York, NY",
    "industry": "Technology",
    "experience": [
        {
            "title": "Senior Developer",
            "company": "Tech Corp",
            "duration": "2020 - Present",
            "description": "Lead development of enterprise applications"
        },
        {
            "title": "Software Engineer",
            "company": "StartUp Inc",
            "duration": "2018 - 2020",
            "description": "Full-stack development and system architecture"
        }
    ],
    "education": [
        {
            "school": "University of Technology",
            "degree": "Master's in Computer Science",
            "year": "2018"
        }
    ],
    "skills": ["Python", "Data Analysis", "Machine Learning", "Web Development", "API Integration"]
}

# Sidebar for search and filters
with st.sidebar:
    st.header("Search Settings")
    
    # Search input
    search_query = st.text_input("Search Profiles", placeholder="Enter name or keyword")
    
    # Filters
    st.subheader("Filters")
    industry_filter = st.multiselect(
        "Industry",
        ["Technology", "Healthcare", "Finance", "Education", "Other"]
    )
    
    location_filter = st.multiselect(
        "Location",
        ["New York, NY", "San Francisco, CA", "Chicago, IL", "Remote"]
    )
    
    experience_filter = st.slider(
        "Years of Experience",
        0, 20, (0, 20)
    )

# Main content
st.markdown('<p class="big-font">Professional Profile Dashboard</p>', unsafe_allow_html=True)

# Profile header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"## {mock_profile['name']}")
    st.markdown(f"*{mock_profile['headline']}*")
    st.markdown(f"📍 {mock_profile['location']} | 🏢 {mock_profile['industry']}")

# Experience section
st.header("Experience")
for exp in mock_profile['experience']:
    with st.expander(f"{exp['title']} at {exp['company']}", expanded=True):
        st.markdown(f"**Duration:** {exp['duration']}")
        st.markdown(exp['description'])

# Education section
st.header("Education")
for edu in mock_profile['education']:
    st.markdown(f"**{edu['school']}**")
    st.markdown(f"{edu['degree']} ({edu['year']})")

# Skills section
st.header("Skills")
skills_cols = st.columns(3)
for idx, skill in enumerate(mock_profile['skills']):
    with skills_cols[idx % 3]:
        st.button(skill, key=f"skill_{idx}")

# Analytics section
st.header("Profile Analytics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Profile Views", "1,234", "+12%")
with col2:
    st.metric("Search Appearances", "567", "+8%")
with col3:
    st.metric("Connection Rate", "76%", "-2%")

# Activity chart
st.subheader("Profile Activity")
activity_data = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
    'Views': np.random.randint(10, 100, 30)
})
st.line_chart(activity_data.set_index('Date'))

# Footer
st.markdown("---")
st.markdown("*This is a demo dashboard. Connect real data sources for production use.*")
