Final Project- Git Pages : https://cohensh96.github.io/Rank-Rangers--Information-Retrieval/

# 🔎 Rank Rangers – Information Retrieval Web System

**Rank Rangers** is an intelligent information retrieval platform that simulates a real-world search engine workflow. It demonstrates how user queries can be transformed into actionable web crawls, filtered and ranked results, and an interactive user interface for reviewing relevance.

👉 [🌐 Live Site](https://cohensh96.github.io/Rank-Rangers--Information-Retrieval/FinalProjectDisplay.html)

---

## 🎯 Project Purpose

This academic project simulates an end-to-end search engine using:
- Query analysis
- Intelligent web crawling
- Data filtering
- Ranking mechanisms
- Results visualization

It was developed as part of an **Information Retrieval** course, aiming to explore how search systems can extract relevant answers to complex natural language queries from the web.

---

## ⚙️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Crawler & Preprocessing Scripts)
- **Data Processing:** Pandas, OpenAI's GPT API, BeautifulSoup
- **Deployment:** GitHub Pages

---

## 🔍 How It Works

### 1️⃣ User Enters a Query

Users can input a question or topic of interest, such as:

> _"What are the available healthcare policies for chronic diseases in Germany?"_

The system then initiates the crawling and retrieval process.

---

### 2️⃣ Web Crawling & Extraction

Python crawler scripts collect relevant data from trusted sources across the web. BeautifulSoup is used to parse HTML and extract textual content.

---

### 3️⃣ Ranking by Relevance

Each snippet is passed through a GPT-based scoring mechanism, ranking it by contextual relevance to the original query.

---

### 4️⃣ Results Display

A clean web UI presents the final ranked list of relevant text chunks, allowing users to quickly identify valuable information.

---

## 📊 Sample Use Case

**Query:** _"What are the available healthcare policies for chronic diseases in Germany?"_

**Pipeline:**
- Crawl 5–10 websites
- Clean and preprocess text
- Score relevance via GPT
- Display ranked snippets in browser

Check out the [results spreadsheet](./results_query_What%20are%20the%20available%20healthcare%20policies%20for%20chronic%20diseases%20in%20Germany%3F.xlsx) for example outputs.

---

## 🧠 Project Highlights

- Combines traditional IR techniques with modern LLM-powered relevance scoring
- Automates end-to-end flow from query → web → output
- Teaches the value of clean data preprocessing in real-world crawling
- Custom ranking based on semantic similarity

---

## 📁 Project Structure

```
/Rank-Rangers--Information-Retrieval/
├── FinalProjectDisplay.html     # Main Web UI
├── crawler_query1.py            # Core web crawler
├── crawler_query1.ipynb         # Crawler in Jupyter format
├── initial_results.xlsx         # Baseline results
├── results_query_*.xlsx         # Final ranked results
```

---

> _“In the era of data abundance, the power lies not in searching – but in retrieving the right answer.”_

