# movie-recom-sys-ml-project
TMDV Movie Recommendation System
By Souvik Sarkar

A content-based movie recommender built in Python using Machine Learning techniques on the TMDB 5000 dataset. Users enter a movie title and the system returns the top 5 most similar movies based on tags extracted from metadata, cast, crew, keywords, and plot overview.

Table of Contents
Project Overview
Dataset
Preprocessing
Feature Engineering
Recommendation Pipeline
Installation & Setup
Usage
Project Structure
Future Work
License
1. Project Overview
This notebook demonstrates a content-based recommendation system:

Merge tmdb_5000_movies.csv and tmdb_5000_credits.csv on title.
Parse JSON-like columns (genres, keywords, cast, crew) to extract only names.
Select top 3 billed cast members and the director.
Clean and normalize text (remove spaces, lowercase, stemming).
Combine all textual features into a single tags column.
Vectorize tags using CountVectorizer (max features = 5000, English stopwords).
Compute pairwise cosine similarity.
Given a movie title, fetch top-5 recommendations.
2. Dataset
Files required (place in a data/ folder):

tmdb_5000_movies.csv
tmdb_5000_credits.csv
TMDB 5000 Dataset source:
https://www.kaggle.com/tmdb/tmdb-movie-metadata

3. Preprocessing
Load CSVs with pandas.
Merge on title:
Python

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
merged = movies.merge(credits, on='title')
Select relevant columns:
movie_id, title, overview, genres, keywords, cast, crew.
Drop rows with nulls in overview.
Parse JSON strings with ast.literal_eval().
Define converters:
convert() to extract list of genre/keyword names
convert_cast() to take top 3 cast names
director() to extract director name
Apply converters, remove spaces in multi-word names, and split overview into words.
4. Feature Engineering
Tags: Concatenate overview + genres + keywords + cast + crew into one list, then join into a single lowercase string.
Stemming: Use NLTK’s PorterStemmer to reduce words to their root form.
Vectorization:
Python

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
5. Recommendation Pipeline
Compute cosine similarity matrix:
Python

from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(vectors)
Define recommender function:
Python

def recommend(movie_title):
    idx = df[df.title == movie_title].index[0]
    distances = list(enumerate(sim_matrix[idx]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    for i, _ in distances:
        print(df.iloc[i].title)
Example:

recommend('The Dark Knight')
# The Dark Knight Rises
# Batman Begins
# Batman Returns
# Batman Forever
# Batman
6. Installation & Setup
Clone the repo:

git clone https://github.com/yourusername/tmdv-movie-recommender.git
cd tmdv-movie-recommender
Create & activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
Install dependencies:

pip install -r requirements.txt
Download NLTK data (in Python REPL):
Python

import nltk
nltk.download('punkt')
Place the two CSV files in data/ and open the notebook:

jupyter notebook notebooks/MovieRecommender.ipynb
7. Usage
After running the preprocessing and similarity computation cells, you can:

Test recommendations in the notebook with recommend('Movie Title').
Save artifacts for production:
Python

import pickle
pickle.dump(df.to_dict(), open('MovieRecomSYS_dict.pkl','wb'))
pickle.dump(sim_matrix,       open('sim_matrix.pkl','wb'))
Load and query in a separate script:
Python

data = pickle.load(open('MovieRecomSYS_dict.pkl','rb'))
df   = pd.DataFrame.from_dict(data)
sim  = pickle.load(open('sim_matrix.pkl','rb'))

def recommend_from_pickle(title):
    idx = df[df.title == title].index[0]
    dists = list(enumerate(sim[idx]))
    top5 = sorted(dists, key=lambda x: x[1], reverse=True)[1:6]
    return [df.iloc[i].title for i,_ in top5]
8. Project Structure

├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── notebooks/
│   └── MovieRecommender.ipynb
├── requirements.txt
├── MovieRecomSYS_dict.pkl
├── sim_matrix.pkl
└── README.md
9. Future Work
Incorporate user ratings for a hybrid recommender.
Deploy as a REST API (Flask/FastAPI) with a front-end.
Experiment with TF-IDF, word embeddings or transformer-based encodings.
Add caching and real-time recommendations.
10. License
This project is licensed under the MIT License. See the LICENSE file for details.

o4-mini
make it more beautiful and gorgeous for the readme file in gihub


Thought Process
expand
Markdown

Collapse
# 🎬 TMDV Movie Recommendation System  
### Content-Based Recommender Powered by AI/ML  
**By Souvik Sarkar**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/tmdv-movie-recommender.svg)](https://github.com/yourusername/tmdv-movie-recommender/issues)

---

<div align="center">
  <img src="docs/screenshot.png" alt="Demo GIF" width="600"/>
  <p><em>Preview: Top 5 recommendations for “The Dark Knight”</em></p>
</div>

---

## 🚀 Quick Start

# Results
![Screenshot 2025-06-25 172545](https://github.com/user-attachments/assets/4c39d283-2e5a-4296-9566-675a9cc55b5d)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/tmdv-movie-recommender.git
cd tmdv-movie-recommender

# 2. Create & activate virtual env
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data (once)
python -c "import nltk; nltk.download('punkt')"

# 5. Place CSV files in data/
#    ├── tmdb_5000_movies.csv
#    └── tmdb_5000_credits.csv

# 6. Launch Jupyter Notebook
jupyter notebook notebooks/MovieRecommender.ipynb
💡 Features
Data Fusion: Merge TMDB movies & credits by title
Smart Parsing: Extract genres, keywords, top-3 cast & director
Textual Tags: Combine overview, genres, keywords, cast, crew into one “tags” field
NLP Preprocessing:
Remove stop words
Porter stemming
Lowercasing & whitespace cleanup
Vectorization: Bag-of-Words (5,000 features) via CountVectorizer
Similarity Search: Cosine similarity to fetch top-5 related movies
📊 Architecture

Collapse
┌──────────────┐     ┌─────────────────┐     ┌─────────────┐
│   Data Load  │──►──│  Preprocessing  │──►──│  Feature    │
│  (CSV merge) │     │ (clean & parse) │     │ Engineering │
└──────────────┘     └─────────────────┘     └─────┬───────┘
                                                   │
                                                   ▼
                                           ┌─────────────────┐
                                           │  Vectorization  │
                                           │  + Stemming     │
                                           └─────────────────┘
                                                   │
                                                   ▼
                                           ┌─────────────────┐
                                           │  Cosine Similar │
                                           │   Matrix Calc   │
                                           └─────────────────┘
                                                   │
                                                   ▼
                                           ┌─────────────────┐
                                           │ Recommendations │
                                           │  (Top-5 Titles) │
                                           └─────────────────┘
📂 Project Structure

tmdv-movie-recommender/
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── notebooks/
│   └── MovieRecommender.ipynb
├── models/
│   ├── sim_matrix.pkl
│   └── movies_dict.pkl
├── requirements.txt
├── README.md
└── LICENSE
🎯 Usage
1. Interactive Notebook
Run through preprocessing, vectorization, similarity and tests in Jupyter:

Python

from recommender import recommend
recommend('The Dark Knight')
# → The Dark Knight Rises
#   → Batman Begins
#   → Batman Returns
#   → Batman Forever
#   → Batman
2. Production Script
Load pickled artifacts and query in any Python script:

Python

Collapse
import pickle
import pandas as pd

# Load
movies_dict = pickle.load(open('models/movies_dict.pkl','rb'))
sim_matrix  = pickle.load(open('models/sim_matrix.pkl','rb'))
df = pd.DataFrame.from_dict(movies_dict)

# Recommender
def recommend(title, top_k=5):
    idx = df[df.title==title].index[0]
    sims = list(enumerate(sim_matrix[idx]))
    sims_sorted = sorted(sims, key=lambda x: x[1], reverse=True)[1:top_k+1]
    return [df.iloc[i].title for i,_ in sims_sorted]

print(recommend('Life of Pi'))
🔭 Future Enhancements
Blend collaborative filtering (user ratings) with content model → Hybrid
Experiment with TF-IDF or word embeddings (Word2Vec/BERT)
Expose as REST API using FastAPI or Flask
Add live user feedback and implicit signals


