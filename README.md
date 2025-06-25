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

1. Load and Merge Data
Load CSV files: Import tmdb_5000_movies.csv and tmdb_5000_credits.csv using pandas.
Merge datasets: Combine these datasets on the title column to create a comprehensive dataframe.

import pandas as pd

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')
merged = movies.merge(credits, on='title')


2. Select and Clean Columns
Select relevant columns: From the merged dataset, keep only movie_id, title, overview, genres, keywords, cast, and crew.
Drop missing overviews: Remove rows where overview is missing to ensure complete data.

df = merged[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
df.dropna(subset=['overview'], inplace=True)

3. Parse JSON Columns
Convert JSON strings: Use ast.literal_eval() to parse genres, keywords, cast, and crew JSON-like strings into Python objects.
Extract names: Retrieve the name field from each list of dictionaries.

Python

import ast

def parse_names(json_str):
    return [i['name'] for i in ast.literal_eval(json_str)]

df['genres'] = df['genres'].apply(parse_names)
df['keywords'] = df['keywords'].apply(parse_names)

4. Extract Top Cast and Director
Top 3 cast: Extract the names of the top 3 billed cast members.
Director: Extract the director's name from the crew.
Python

Python

def top_cast(json_str, n=3):
    return [i['name'] for i in ast.literal_eval(json_str)][:n]

def get_director(json_str):
    for i in ast.literal_eval(json_str):
        if i['job'] == 'Director':
            return [i['name']]
    return []

df['cast'] = df['cast'].apply(top_cast)
df['crew'] = df['crew'].apply(get_director)

5. Normalize and Tokenize Text
Remove spaces: Eliminate spaces in multi-word tokens.
Lowercase tokens: Convert all text to lowercase.
Tokenize overview: Split the overview into individual words.

for col in ['genres', 'keywords', 'cast', 'crew']:
    df[col] = df[col].apply(lambda lst: [name.replace(' ', '') for name in lst])

df['overview'] = df['overview'].apply(lambda x: x.split())

6. Build the “Tags” Feature
Concatenate features: Combine overview, genres, keywords, cast, and crew into a single tags field.
Lowercase and join: Convert the list of tokens into a single lowercase string.

df['tags'] = (
    df['overview'] +
    df['genres'] +
    df['keywords'] +
    df['cast'] +
    df['crew']
).apply(lambda lst: " ".join(lst).lower())

7. Stemming and Vectorization
Apply stemming: Use NLTK’s PorterStemmer to stem words in the tags field.
Vectorize text: Convert tags into vectors using CountVectorizer with 5,000 features.

from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def stem(text):
    return " ".join(ps.stem(word




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

# After creating a app using streamlit it looks like
( here 'surprise me' and 'hidden gem' are to magical buttons to know more go to the website and know about it ) 
# results
![Screenshot 2025-06-25 172545](https://github.com/user-attachments/assets/cd456be6-c7a2-4d4b-8010-c5fe9644c6be)

