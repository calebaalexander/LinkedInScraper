import streamlit as st
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Analyzer",
    page_icon="📊",
    layout="wide"
)

# Sidebar inputs
with st.sidebar:
    st.header("Profile Search")
    
    # LinkedIn URL input
    linkedin_url = st.text_input(
        "Enter LinkedIn URL",
        placeholder="www.linkedin.com/in/username"
    )
    
    st.markdown("---")
    
    # Keyword search
    st.header("Content Search")
    search_term = st.text_input(
        "Search profile content",
        placeholder="Enter keyword (e.g. 'analytics')"
    )

# Mock profile data - replace with actual API data in production
def get_profile_data(url):
    # This would be replaced with actual API calls
    return {
        "name": "Caleb A. Alexander",
        "current_role": "Professor of Epidemiology and Medicine",
        "experience_years": 15,
        "education": "Johns Hopkins Bloomberg School of Public Health",
        "full_text": """
        Founding Director of the Center for Drug Safety and Effectiveness.
        Professor of Epidemiology and Medicine at Johns Hopkins.
        Focuses on pharmaceutical analytics and drug safety research.
        Conducts population-based studies using analytics methods.
        Expertise in pharmacoepidemiology and health services research.
        Uses advanced analytics for drug utilization studies.
        """
    }

# Main content area
if linkedin_url:
    profile_data = get_profile_data(linkedin_url)
    
    # Display key profile information
    st.header("Profile Summary")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {profile_data['name']}")
        st.markdown(f"**Current Role:** {profile_data['current_role']}")
        st.markdown(f"**Years of Experience:** {profile_data['experience_years']}")
        st.markdown(f"**Education:** {profile_data['education']}")

    # Handle keyword search
    if search_term:
        st.markdown("---")
        st.header(f"Search Results for '{search_term}'")
        
        # Search through profile text
        text = profile_data['full_text']
        sentences = text.split('.')
        found = False
        
        for sentence in sentences:
            if search_term.lower() in sentence.lower():
                found = True
                # Highlight the search term
                highlighted = re.sub(
                    f'({search_term})',
                    r'**\1**',
                    sentence,
                    flags=re.IGNORECASE
                )
                st.markdown(f"• {highlighted.strip()}")
        
        if not found:
            st.info(f"No mentions of '{search_term}' found in the profile.")

else:
    st.info("👈 Enter a LinkedIn URL in the sidebar to start analyzing a profile")

# Footer
st.markdown("---")
st.markdown("*Note: This is a demo using mock data. Connect to appropriate APIs for production use.*")
