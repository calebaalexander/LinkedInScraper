import streamlit as st
import requests
import json
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Profile Analyzer",
    page_icon="📊",
    layout="wide"
)

def fetch_business_data(business_id, photo_id):
    """
    Fetch data from RapidAPI local-business-data endpoint
    """
    url = "https://local-business-data.p.rapidapi.com/photo-details"
    
    querystring = {
        "business_id": business_id,
        "photo_id": photo_id
    }
    
    headers = {
        "X-RapidAPI-Key": "e76e6d59aamshd5745b36f1e312ap1a642ejsn4a367f21a64c",
        "X-RapidAPI-Host": "local-business-data.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an exception for bad status codes
        st.write("API Response:", response.json())  # Debug output
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar for search
with st.sidebar:
    st.header("Profile Search")
    
    # Profile URL input
    profile_url = st.text_input(
        "Enter Profile URL",
        value="https://www.linkedin.com/in/caleb-a-alexander/",
        help="Enter the full URL of the profile"
    )

    # API Testing Section
    st.markdown("---")
    st.header("API Test Parameters")
    business_id = st.text_input(
        "Business ID",
        value="0x89c259b5a9bd152b:0x31453e62a3be9f76"
    )
    photo_id = st.text_input(
        "Photo ID",
        value="AF1QipMPYCqZ5Fe8a7Jc51KT9pWOS5c6tOKY_xvkCl23"
    )
    
    if st.button("Test API Connection"):
        with st.spinner("Testing API connection..."):
            result = fetch_business_data(business_id, photo_id)
            if result:
                st.success("API connection successful!")
                st.json(result)
            else:
                st.error("API connection failed")
    
    st.markdown("---")
    
    # Content search
    st.header("Content Search")
    search_query = st.text_input(
        "Search profile content",
        placeholder="Enter keyword to search"
    )

# Main content area for profile display
if profile_url:
    st.header("Profile Data")
    
    # Display raw API response for debugging
    st.subheader("Raw API Response")
    result = fetch_business_data(business_id, photo_id)
    if result:
        st.json(result)
    
    # Add search functionality
    if search_query:
        st.markdown("---")
        st.header(f"Search Results for '{search_query}'")
        if result:
            # Search through the API response data
            json_str = json.dumps(result)
            if search_query.lower() in json_str.lower():
                st.success(f"Found '{search_query}' in the data!")
                # You can implement more sophisticated search here
            else:
                st.info(f"No matches found for '{search_query}'")

# Footer
st.markdown("---")
st.markdown("*Using RapidAPI local-business-data endpoint*")
