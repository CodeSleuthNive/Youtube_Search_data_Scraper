from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import streamlit as st
import base64


st.header("YouTube Search Results Scraper")

# -------------------------------
# Streamlit form for user inputs
# -------------------------------
with st.form("youtube_search_form"):
    search_query = st.text_input('Enter Search Keyword')
    scroll_count = st.text_input('Enter Number of Scrolls (Default = 25)', value='25')
    scroll_count = int(scroll_count)

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write("PROCESSING... PLEASE WAIT")

        if not search_query.strip():
            st.warning("Please enter a valid search term.")
            st.stop()

        progress_bar = st.progress(0, text="STARTED")

        # -------------------------------
        # Set up Chrome WebDriver (Headless)
        # -------------------------------
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", chrome_prefs)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.youtube.com")

        # -------------------------------
        # Perform YouTube search
        # -------------------------------
        search_box = driver.find_element_by_name('search_query')
        search_box.send_keys(search_query)
        search_box.submit()

        # -------------------------------
        # Scroll to load results
        # -------------------------------
        SCROLL_PAUSE_TIME = 1.5
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        scroll_counter = 0
        while scroll_counter < scroll_count:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_counter += 1

        time.sleep(10)  # wait for content to load

        # -------------------------------
        # Extract video details
        # -------------------------------
        video_elements = driver.find_elements_by_css_selector('ytd-video-renderer')
        video_data = []

        for element in video_elements:
            lines = element.text.split("\n")
            if len(lines[0]) < 9:
                lines = lines[1:]

            video_link = element.find_element_by_id("video-title").get_attribute('href')
            channel_link = element.find_element_by_id("channel-thumbnail").get_attribute('href')

            if len(lines) == 5:
                video_data.append({
                    'Title': lines[0],
                    'Views': lines[1],
                    'Published': lines[2],
                    'Channel_Name': lines[3],
                    'Description': lines[4],
                    'Channel_Link': channel_link,
                    'Video_Link': video_link
                })
            else:
                video_data.append({
                    'Title': lines[0],
                    'Views': lines[1],
                    'Published': lines[2],
                    'Channel_Name': None,
                    'Description': None,
                    'Channel_Link': channel_link,
                    'Video_Link': video_link
                })

        # -------------------------------
        # Create DataFrame
        # -------------------------------
        results_df = pd.DataFrame(video_data)

        # Helper functions
        def extract_video_id(url):
            try:
                return url.split('=')[1][:11]
            except Exception:
                return url[-11:]

        def classify_video_type(url):
            try:
                url.split('=')[1][:11]
                return "VIDEO"
            except Exception:
                return "SHORTS"

        results_df["Video_ID"] = results_df['Video_Link'].apply(extract_video_id)
        results_df["Content_Type"] = results_df['Video_Link'].apply(classify_video_type)
        results_df["Search_Query"] = search_query

        # -------------------------------
        # Display results
        # -------------------------------
        st.header("Scraping Results")

        st.subheader(f"Total Results: {len(results_df)}")
        st.subheader(f"Total Videos: {len(results_df[results_df['Content_Type'] == 'VIDEO'])}")
        st.subheader(f"Total Shorts: {len(results_df[results_df['Content_Type'] == 'SHORTS'])}")

        st.subheader("Extracted Data")
        st.dataframe(results_df)

        # -------------------------------
        # CSV Download Function
        # -------------------------------
        def download_csv_link(df):
            csv_data = df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="youtube_search_results.csv">Download CSV file</a>'
            return href

        st.markdown(download_csv_link(results_df), unsafe_allow_html=True)

        driver.quit()
