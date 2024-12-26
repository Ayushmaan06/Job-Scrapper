import streamlit as st
import pandas as pd
from PIL import Image
import requests
import subprocess
import os

# Streamlit Configuration
st.set_page_config(page_title="Job Listings", layout="wide")

# Title and Introduction
st.title("Job Scraping Frontend")
st.write("Enter the required inputs to scrape job listings.")

# Input Fields
scrolls = st.number_input("Enter the number of scrolls:", min_value=1, step=1)
job_ts = st.text_input("Enter the job title to search for:")

# Run Backend
if st.button("Run Scraper"):
    if job_ts.strip() == "":
        st.error("Please enter a job title.")
    else:
        # Run the backend file with inputs
        try:
            result = subprocess.run(
                ["python", "backend_file.py", str(scrolls), job_ts],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success("Job scraping completed successfully!")
            else:
                st.error("An error occurred while running the scraper.")
                st.text(result.stderr)
        except Exception as e:
            st.error(f"Failed to run scraper: {e}")

# Display Scraped Data with Filters
if os.path.exists("job_cards.csv"):
    st.write("### Job Listings:")
    df = pd.read_csv("job_cards.csv")

    # Add filters
    job_title_filter = st.text_input("Search by Job Title", "")
    company_filter = st.text_input("Search by Company", "")
    location_filter = st.text_input("Search by Location", "")

    # Apply filters
    filtered_df = df

    if job_title_filter:
        filtered_df = filtered_df[filtered_df['Job Title'].str.contains(job_title_filter, case=False, na=False)]

    if company_filter:
        filtered_df = filtered_df[filtered_df['Company'].str.contains(company_filter, case=False, na=False)]

    if location_filter:
        filtered_df = filtered_df[filtered_df['Location'].str.contains(location_filter, case=False, na=False)]

    # Display filtered results
    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            col1, col2 = st.columns([1, 3])

            # Display job image
            with col1:
                try:
                    img = Image.open(requests.get(row['Image URL'], stream=True).raw)
                    st.image(img, use_container_width=True)
                except Exception:
                    st.image("https://via.placeholder.com/150", use_container_width=True)

            # Display job details
            with col2:
                st.subheader(f"[{row['Job Title']}]({row['Job URL']})")
                st.write(f"**Company**: {row['Company']}")
                st.write(f"**Location**: {row['Location']}")
                st.write(f"[Apply Here]({row['Job URL']})")
    else:
        st.write("No jobs found with the given filters.")
else:
    st.write("No data available yet. Run the scraper to generate job listings.")
