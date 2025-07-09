import pandas as pd
import numpy as np
import re
import string
import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords une seule fois
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Charger les données issues du scraping
df = pd.read_csv("amazon_resultats.csv")

#  1. Nettoyage des données brutes
df = df.drop_duplicates()
df = df.dropna(subset=["titre"])

# Supprimer les faux blocs ou pubs
filtres = ["Results", "highlighted", "Check", "Pick", "sponsored", "buying options"]
pattern_filtre = '|'.join(filtres)
df = df[~df["titre"].str.contains(pattern_filtre, case=False, na=False)]

# Supprimer les titres trop courts
df = df[df["titre"].str.len() > 10]

#  2. Nettoyage du texte
def clean_text(text):
    text = str(text)
    text = unidecode.unidecode(text)                         # enlever les accents
    text = text.lower()                                      # tout en minuscules
    text = re.sub(r'\d+', '', text)                          # supprimer les chiffres
    text = text.translate(str.maketrans('', '', string.punctuation))  # supprimer ponctuation
    words = text.split()
    words = [w for w in words if w not in stop_words]        # supprimer stopwords
    return " ".join(words)

df["titre_nettoye"] = df["titre"].apply(clean_text)

# 3. Générer des labels aléatoires (juste pour test)
df["label"] = np.random.randint(0, 2, size=len(df))

#  4. Sauvegarder
df.to_csv("avis_labellises.csv", index=False)

#  5. Affichage de contrôle
print(df[["titre", "titre_nettoye", "label"]].head())
print(f"\n Nettoyage et labellisation terminés : {len(df)} lignes enregistrées dans 'avis_labellises.csv'")
