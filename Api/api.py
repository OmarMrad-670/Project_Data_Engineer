from fastapi import FastAPI
from typing import List
import pandas as pd
from detoxify import Detoxify
from pymongo import MongoClient

import re
#import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


app = FastAPI()



# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["comment_database"]
collection = db["comment_collection"]



# Charger le modèle Detoxify
detoxify_model = Detoxify('original')



# Charger les données CSV
data = pd.read_csv("data_twitts.csv")


#Nettoyage des donnees
def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        # Supprimer les URLs
        comment = re.sub(r'http\S+', '', str(comment))
        # Convertir en minuscules
        comment = comment.lower()
        # Tokenization
        tokens = word_tokenize(comment)
        # Supprimer les mots vides
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        # Lemmatisation
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # Reconstruire le commentaire
        cleaned_comment = ' '.join(tokens)
        cleaned_comments.append(cleaned_comment)
    return cleaned_comments


# Fonction pour analyser la toxicité des commentaires
def analyze_toxicity(comments):
    toxicities = detoxify_model.predict(comments)
    return toxicities


@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de votre application!"}


@app.get("/analyze_comments/")
@app.post("/analyze_comments/")
def analyze_comments():
    # Nettoyer les commentaires
    cleaned_text = clean_comments(data["text"])
    
    # Analyser la toxicité des commentaires
    toxicities = analyze_toxicity(cleaned_text)
    
    # Enregistrer les résultats dans MongoDB
    for text, toxicity in zip(cleaned_text, toxicities):
        comment_data = {
            "text": text,
            "toxicity": toxicity
        }
        # Insérer les données dans MongoDB
        collection.insert_one(comment_data)
    
    return {"message": "Analyse des commentaires terminée"}




#if __name__ == "__main__":
    #import uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=8001)






