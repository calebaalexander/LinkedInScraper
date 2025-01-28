import streamlit as st
import requests
import json
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Analyzer",
    page_icon="👔",
    layout="wide"
)

def fetch_linkedin_data(profile_url):
    """
    Fetch data from Fresh LinkedIn Profile Data API
    """
    headers = {
        "X-RapidAPI-Key": "e76e6d59aamshd5745b36f1e312ap1a642ejsn4a367f21a64c",
        "X-RapidAPI-Host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    
    # Encode the LinkedIn URL
    encoded_url = quote(profile_url)
    
    api_url = f"https://fresh-linkedin-profile-data.p.rapidapi.com/get-job-details?job_url={encoded_url}&include_skills=false&include_hiring_team=false"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar for search
with st.sidebar:
    st.header("Profile Search")
    
    # LinkedIn URL input
    profile_url = st.text_input(
        "Enter LinkedIn URL",
        placeholder="https://www.linkedin.com/in/username",
        help="Enter the full LinkedIn profile URL"
    )
    
    # Search functionality
    st.markdown("---")
    st.header("Content Search")
    search_query = st.text_input(
        "Search profile content",
        placeholder="Enter keyword to search"
    )

# Main content area
if profile_url:
    st.header("Profile Data")
    
    with st.spinner("Fetching profile data..."):
        profile_data = fetch_linkedin_data(profile_url)
        
        if profile_data:
            # Display key profile information
            st.subheader("Profile Information")
            try:
                col1, col2 = st.columns(2)
                with col1:
                    if 'job_title' in profile_data:
                        st.markdown(f"**Job Title:** {profile_data['job_title']}")
                    if 'company' in profile_data:
                        st.markdown(f"**Company:** {profile_data['company']}")
                with col2:
                    if 'location' in profile_data:
                        st.markdown(f"**Location:** {profile_data['location']}")
                    if 'employment_type' in profile_data:
                        st.markdown(f"**Employment Type:** {profile_data['employment_type']}")
                
                # Display job description if available
                if 'description' in profile_data:
                    st.subheader("Job Description")
                    st.markdown(profile_data['description'])
                
                # Handle search functionality
                if search_query:
                    st.subheader(f"Search Results for '{search_query}'")
                    json_str = json.dumps(profile_data, indent=2).lower()
                    content_str = str(profile_data.get('description', '')).lower()
                    
                    if search_query.lower() in content_str:
                        # Split into sentences and highlight matches
                        sentences = content_str.split('.')
                        for sentence in sentences:
                            if search_query.lower() in sentence:
                                st.markdown(f"• ...{sentence.strip()}...")
                    else:
                        st.info(f"No matches found for '{search_query}'")
                
                # Raw data (collapsible)
                with st.expander("View Raw API Response"):
                    st.json(profile_data)
                
            except KeyError as e:
                st.error(f"Error parsing profile data: {str(e)}")
        else:
            st.error("Failed to fetch profile data. Please check the URL and try again.")

else:
    st.info("👈 Enter a LinkedIn profile URL in the sidebar to begin analysis")

# Footer
st.markdown("---")
st.markdown("*Using Fresh LinkedIn Profile Data API via RapidAPI*")
