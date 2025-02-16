# YouTube-Comment-Scraper

## 📌 About This Project

This project is a Python-based web scraper that extracts YouTube comments from videos using the YouTube Data API v3. The scraped data can be used for text-classification, bot detection, and other NLP (Natural Language Processing) tasks.
Read more about my project @ https://daniwave100.github.io/DanielPersonalPage/ !

## 🔍 Features

- ✔ Efficient Data Extraction – Uses the YouTube Data API to scrape comments from any public video
- ✔ Structured Data Output – Stores extracted comments in a CSV file
- ✔ User-friendly front-end interface

## 🛠️ Tech Stack
	-	Python – Core programming language
	-	Google YouTube Data API v3 – Fetches comments from YouTube videos
	-	Pandas – Organizes and processes extracted data
	-	Requests – Handles API calls and data retrieval
	-	Flask - Integrates a web-based UI for ease of use

## 📊 How it Works
  - 1️⃣ User Inputs Video ID – The program takes a valid YouTube video ID as input
  - 2️⃣ API Fetches Comments – The script uses the YouTube Data API to collect comments and metadata
  - 3️⃣ Handles Pagination – The scraper automatically loops through API pages to extract all available comments
  - 4️⃣ Stores in CSV – The extracted data (username, comment, date, etc.) is stored in a structured CSV file for further processing

 ## 📈 Future Improvements
  - ✅ JavaScript error-handling – Improve user-expierience with better error-handling and cleaner interface 
  - ✅ Expand Scraping Capabilities – Extract more metadata (Perhaps use profile pictures as a training  parameter?)
  - ✅ Integrate with my AI Model – Directly send extracted data into an AI classifier to train model and detect bot-generated comments (ROC curves, classifier matrix)

## ⚠️ Current Development Status

💡 Future iterations will focus on making this tool more robust by integrating real-time AI classification, a web-based UI, and better data visualization tools.
