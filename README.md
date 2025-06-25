🎬 TMDV Movie Recommendation System & Web App
By Souvik Sarkar

A content-based movie recommender built in Python (pandas, scikit-learn, NLTK) and exposed via a Flask web application. Enter any movie title and get the top 5 similar films—complete with posters!

📖 Table of Contents
Overview
Features
Tech Stack
Dataset
Installation
Notebook Step-by-Step
Web Application
Screenshots
Future Work
Contributing
License
Overview
This project demonstrates a content-based recommender using the TMDB 5000 dataset. We merge movie metadata & credits, parse genres/keywords/cast/crew, build a “tags” feature, vectorize text, compute cosine similarity, and expose recommendations via a Flask web app.

Features
Merge tmdb_5000_movies.csv + tmdb_5000_credits.csv by title
Parse JSON fields: genres, keywords, cast, crew
Extract top-3 cast members & director
Text cleaning: remove spaces, lowercase, tokenize, Porter stemming
Combine overview + genres + keywords + cast + crew → tags
Bag-of-Words vectorization (5,000 features)
Cosine similarity scoring
Flask UI: search by title, display 5 recommendations with posters
Tech Stack
Python 3.8+
pandas, NumPy
scikit-learn
NLTK (PorterStemmer)
Flask, Jinja2, Bootstrap
Dataset
Place these files in data/

tmdb_5000_movies.csv
tmdb_5000_credits.csv
Download from Kaggle: https://www.kaggle.com/tmdb/tmdb-movie-metadata

Installation
Clone repo
BASH

git clone https://github.com/yourusername/tmdv-movie-recommender.git
cd tmdv-movie-recommender
Create & activate virtual environment
BASH

python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
Install dependencies
BASH

pip install -r requirements.txt
Download NLTK punkt tokenizer
BASH

python -c "import nltk; nltk.download('punkt')"
Notebook Step-by-Step
Open notebooks/MovieRecommender.ipynb and run each cell:

Load & Merge Data
Python

import pandas as pd
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')
merged = movies.merge(credits, on='title')
Select & Clean Columns
Python

df = merged[['movie_id','title','overview','genres','keywords','cast','crew']]
df.dropna(subset=['overview'], inplace=True)
Parse JSON Columns
Python

import ast
def parse_names(x):
    return [i['name'] for i in ast.literal_eval(x)]
df['genres']   = df['genres'].apply(parse_names)
df['keywords'] = df['keywords'].apply(parse_names)
Extract Top Cast & Director
Python

def top_cast(x, n=3):
    return [i['name'] for i in ast.literal_eval(x)][:n]
def get_director(x):
    for i in ast.literal_eval(x):
        if i['job']=='Director':
            return [i['name']]
    return []
df['cast'] = df['cast'].apply(top_cast)
df['crew'] = df['crew'].apply(get_director)
Normalize & Tokenize
Python

# remove spaces in multi-word names
for col in ['genres','keywords','cast','crew']:
    df[col] = df[col].apply(lambda lst: [name.replace(' ','') for name in lst])
# tokenize overview into words
df['overview'] = df['overview'].apply(lambda x: x.split())
Build “tags” Feature
Python

df['tags'] = df['overview'] + df['genres'] + df['keywords'] + df['cast'] + df['crew']
df['tags'] = df['tags'].apply(lambda lst: " ".join(lst).lower())
Stemming & Vectorization
Python

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
df['tags'] = df['tags'].apply(lambda txt: " ".join(ps.stem(w) for w in txt.split()))

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
Compute Cosine Similarity
Python

from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(vectors)
Recommendation Function
Python

def recommend(title, top_k=5):
    idx = df[df.title==title].index[0]
    scores = list(enumerate(sim_matrix[idx]))
    top = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_k+1]
    return [df.iloc[i].title for i,_ in top]
Save Model Artifacts
Python

import pickle
pickle.dump(df.to_dict(), open('models/movies_dict.pkl','wb'))
pickle.dump(sim_matrix,    open('models/sim_matrix.pkl','wb'))
Web Application
Project Structure

Collapse
tmdv-movie-recommender/
├── app.py
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── models/
│   ├── movies_dict.pkl
│   └── sim_matrix.pkl
├── notebooks/
│   └── MovieRecommender.ipynb
├── requirements.txt
├── static/
│   └── css/styles.css
├── templates/
│   └── index.html
└── README.md
Configuration
In app.py, set paths to movies_dict.pkl and sim_matrix.pkl. Optionally configure TMDB API key & poster base URL.

Running Locally
BASH

# Activate venv, ensure models are generated
python app.py
Browse to http://127.0.0.1:5000/, enter a title, and view 5 recommendations with poster images.

Endpoints
GET / — Homepage with search form
POST /recommend — Returns JSON:
JSON

{
  "recommendations": [
    {"title":"Batman Begins","poster_url": "..."},
    ...
  ]
}
Screenshots
Homepage
Enter a movie title and hit “Recommend”

Results
Top 5 similar movies with posters

Future Work
Hybrid recommender using collaborative filtering
TF-IDF or deep embeddings (Word2Vec, BERT)
Deploy via Docker + Gunicorn + NGINX
Front-end SPA (React/Vue)
Contributing
Fork & clone
Create branch: git checkout -b feature/YourFeature
Commit: git commit -m "Add feature"
Push & open PR
# results
![Screenshot 2025-06-25 172545](https://github.com/user-attachments/assets/cd456be6-c7a2-4d4b-8010-c5fe9644c6be)

