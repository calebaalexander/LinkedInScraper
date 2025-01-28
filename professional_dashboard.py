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
    
    try:
        # Use the base endpoint for profile data
        api_url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile"
        
        # Set up query parameters
        params = {
            "linkedin_url": profile_url,
            "include_skills": "false"
        }
        
        # Make the request
        response = requests.get(api_url, headers=headers, params=params)
        
        # Debug information
        st.sidebar.write("Debug - API URL:", response.url)
        st.sidebar.write("Debug - Status Code:", response.status_code)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        st.error(f"Full URL: {response.url}")
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
            try:
                # Display key profile information
                st.subheader("Profile Information")
                
                # Profile header with image
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if 'profile_pic_url' in profile_data:
                        st.image(profile_data['profile_pic_url'], width=200)
                    else:
                        # Display a placeholder avatar
                        st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y", width=200)
                
                # Main profile information
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'full_name' in profile_data:
                        st.markdown(f"**Name:** {profile_data['full_name']}")
                    if 'headline' in profile_data:
                        st.markdown(f"**Headline:** {profile_data['headline']}")
                    if 'location' in profile_data:
                        st.markdown(f"**Location:** {profile_data['location']}")
                
                with col2:
                    if 'current_company' in profile_data:
                        st.markdown(f"**Current Company:** {profile_data['current_company']}")
                    if 'connections' in profile_data:
                        st.markdown(f"**Connections:** {profile_data['connections']}")
                
                # Experience section
                if 'experiences' in profile_data:
                    st.subheader("Experience")
                    for exp in profile_data['experiences']:
                        with st.expander(f"{exp.get('title', 'Role')} at {exp.get('company', 'Company')}"):
                            st.markdown(f"**Duration:** {exp.get('date_range', 'N/A')}")
                            st.markdown(f"**Location:** {exp.get('location', 'N/A')}")
                            if 'description' in exp:
                                st.markdown(exp['description'])
                
                # Education section
                if 'education' in profile_data:
                    st.subheader("Education")
                    for edu in profile_data['education']:
                        st.markdown(f"**{edu.get('school', 'School')}**")
                        st.markdown(f"{edu.get('degree', 'Degree')} ({edu.get('date_range', 'N/A')})")
                
                # Handle search functionality
                if search_query:
                    st.subheader(f"Search Results for '{search_query}'")
                    json_str = json.dumps(profile_data, indent=2).lower()
                    
                    # Search in all text content
                    search_results = []
                    if 'experiences' in profile_data:
                        for exp in profile_data['experiences']:
                            if 'description' in exp and search_query.lower() in exp['description'].lower():
                                search_results.append(f"Found in experience at {exp['company']}: {exp['description']}")
                    
                    if search_results:
                        for result in search_results:
                            st.markdown(f"• {result}")
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
