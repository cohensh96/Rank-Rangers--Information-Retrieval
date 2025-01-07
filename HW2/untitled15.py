# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
from urllib.parse import urljoin
import time
from collections import defaultdict
import math  # For log in IDF
import pandas as pd

class SearchEngine:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = {
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any',
            'are', 'aren', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between',
            'both', 'but', 'by', 'can', 'could', 'did', 'do', 'does', 'doing', 'don', 'down', 'during',
            'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her',
            'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is',
            'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not',
            'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out',
            'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the',
            'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
            'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when',
            'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours',
            'yourself', 'yourselves'
        }
        self.url_to_id = {}
        self.id_to_url = {}
        self.next_id = 1

        # inverted_index[word][doc_id] = count of word in doc
        self.inverted_index = defaultdict(lambda: defaultdict(int))

        # global_index[word][url] = count of word in url
        self.global_index = defaultdict(lambda: defaultdict(int))

    def get_url_id(self, url):
        """Map URLs to unique IDs"""
        if url not in self.url_to_id:
            self.url_to_id[url] = self.next_id
            self.id_to_url[self.next_id] = url
            self.next_id += 1
        return self.url_to_id[url]

    def fetch_page(self, url):
        """Fetch the HTML page content"""
        try:
            time.sleep(1)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def get_links(self, soup, base_url):
        """Extract links from a page"""
        links = set()
        if soup:
            for link in soup.find_all('a', href=True):
                url = link['href']
                absolute_url = urljoin(base_url, url)
                if absolute_url.startswith(base_url):
                    links.add(absolute_url)
        return links

    def index_words(self, soup, url):
        """
        Index words from a page, storing the stemmed form.
        Returns a dictionary of {word: count_in_this_document}.
        """
        index = defaultdict(int)
        url_id = self.get_url_id(url)

        if soup:
            words = re.findall(r'\w+', soup.get_text())
            for word in words:
                word = word.lower()
                if word not in self.stop_words:
                    stemmed_word = self.stemmer.stem(word)

                    # Increase counters in the local index (for this page)
                    index[stemmed_word] += 1

                    # Update the global/inverted index
                    self.inverted_index[stemmed_word][url_id] += 1
                    self.global_index[stemmed_word][url] += 1

        return dict(index)

    def crawl_and_index(self, start_url, max_pages=5):
        """Crawl and index pages. Returns a dict: {doc_id: {word: count}}"""
        visited = set()
        to_visit = {start_url}
        page_indexes = {}

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            if url in visited:
                continue

            print(f"Crawling: {url} (ID: {self.get_url_id(url)})")
            soup = self.fetch_page(url)
            if soup:
                page_indexes[self.get_url_id(url)] = self.index_words(soup, url)
                visited.add(url)
                links = self.get_links(soup, start_url)
                to_visit.update(links - visited)

        return page_indexes

    def save_to_excel(self, page_indexes, filename="results.xlsx"):
        """
        Save:
         1) URL Mappings
         2) Page Word Counts
         3) Top 15 Inverted Index
        """
        # 1) URL Mappings sheet
        url_mappings = [{"URL ID": url_id, "URL": url} for url, url_id in self.url_to_id.items()]
        url_df = pd.DataFrame(url_mappings)

        # 2) Page Word Counts sheet
        rows = []
        for url_id, index in page_indexes.items():
            for word, count in index.items():
                rows.append({"URL ID": url_id, "Word": word, "Count": count})
        counts_df = pd.DataFrame(rows)

        # 3) Calculate global word frequencies to find top 15
        word_frequencies = defaultdict(int)
        for word, docs in self.inverted_index.items():
            word_frequencies[word] = sum(docs.values())

        top_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:15]
        top_words_set = {word for word, _ in top_words}

        # Filter the inverted index for the top 15 words
        inverted_rows = []
        for word, docs in self.inverted_index.items():
            if word in top_words_set:
                document_ids = ", ".join(map(str, docs.keys()))
                inverted_rows.append({"Word": word, "Document IDs": document_ids})
        inverted_df = pd.DataFrame(inverted_rows)

        # Save to Excel (initial sheets)
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            url_df.to_excel(writer, index=False, sheet_name="URL Mappings")
            counts_df.to_excel(writer, index=False, sheet_name="Page Word Counts")
            inverted_df.to_excel(writer, index=False, sheet_name="Top 15 Inverted Index")

        print(f"Results saved to '{filename}'.")

    def calculate_tf_idf_for_query(self, query, page_indexes, filename="results.xlsx"):
        """
        1) Preprocess query (tokenize, remove stopwords, stemming).
        2) For each query word (concept), for each document:
             - Compute TF
             - Compute IDF
             - Compute TF-IDF
        3) Save detailed results (doc_id, url, concept, TF, IDF, TF-IDF) to a new sheet in the Excel file
           with 10 decimal places.
        """
        # 1) Preprocess the query
        query_words = re.findall(r'\w+', query.lower())
        processed_query = []
        for qw in query_words:
            if qw not in self.stop_words:
                stemmed_qw = self.stemmer.stem(qw)
                processed_query.append(stemmed_qw)

        # 2) Collect stats for TF-IDF
        N = len(page_indexes)  # total number of documents
        doc_total_words = {}
        for doc_id, index_dict in page_indexes.items():
            total_count = sum(index_dict.values())
            doc_total_words[doc_id] = total_count

        # 3) Compute TF, IDF, TF-IDF
        tf_idf_rows = []
        for doc_id, index_dict in page_indexes.items():
            url = self.id_to_url[doc_id]
            total_words_in_doc = doc_total_words[doc_id]

            for qw in processed_query:
                freq_in_doc = self.inverted_index[qw].get(doc_id, 0)
                tf = freq_in_doc / total_words_in_doc if total_words_in_doc > 0 else 0.0


                df = len(self.inverted_index[qw].keys())  # number of docs containing qw
                idf = math.log(N / df, 10) if df > 0 else 0.0
                tf_idf = tf * idf

                tf_idf_rows.append({
                    "Document ID": doc_id,
                    "URL": url,
                    "Query Concept": qw,
                    "TF": tf,
                    "IDF": idf,
                    "TF-IDF": tf_idf
                })

        # 4) Create a DataFrame and append to the existing Excel file,
        #    ensuring 10 decimal places in numeric columns.
        tf_idf_df = pd.DataFrame(tf_idf_rows)

        with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            # The 'float_format' parameter ensures up to 10 digits after the decimal point
            tf_idf_df.to_excel(
                writer,
                index=False,
                sheet_name="Query TF-IDF",
                float_format="%.10f"  # ensures 10 places
            )

        print("TF-IDF results for the query have been appended to the Excel file.")

def main():
    search_engine = SearchEngine()

    # 1) Crawl up to 20 pages
    start_url = "https://www.bundesgesundheitsministerium.de/en/"
    page_indexes = search_engine.crawl_and_index(start_url, max_pages=20)

    # 2) Save the initial results
    search_engine.save_to_excel(page_indexes, "results.xlsx")

    # 3) Define the query
    user_query = "What are the average waiting times in hospitals in Germany by region?"

    # 4) Calculate TF-IDF for that query, saving results with 10 decimal precision
    search_engine.calculate_tf_idf_for_query(user_query, page_indexes, "results.xlsx")

if __name__ == "__main__":
    main()