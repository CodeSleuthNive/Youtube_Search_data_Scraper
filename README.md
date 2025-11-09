# YouTube Search Results Scraper
This project is a YouTube video search scraper built with Streamlit and Selenium. It allows users to search YouTube for videos using a keyword, gather video details, and download the data in CSV format.

## Features
### User-Friendly Interface: 
  Users input a search term and set the number of scrolls to control the volume of search results.
### Automated Data Collection: 
  Selenium automatically scrolls the YouTube search page, loading and collecting videos based on the specified number of scrolls.
### Video Data Extraction: 
  For each video found, the app captures details like: Title, Views, Published Date, Channel Name, Description, Channel Link, Video Link
### Video Categorization: 
  Each result is classified as either a regular YouTube video or a "Short" based on the link structure.
### Data Display and CSV Download: 
  The results are displayed in a table, and users can download the data as a CSV file directly from the app.

  
## Usage
* Enter a search term and specify the number of scrolls.
* Click "Submit" to start the search.
* View the results and download them as a CSV file if needed.

  
## Technical Overview
* Selenium WebDriver handles browser automation for scrolling and loading YouTube search results.
* Streamlit provides the interface for user input, data display, and CSV download.
* Pandas organizes data into a table for display and easy export.
* This tool is helpful for gathering YouTube video data quickly, categorizing video types, and providing a structured way to analyze YouTube content based on search results.
