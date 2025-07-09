import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Charger le dataset issu du scraping
df = pd.read_csv("amazon_resultats.csv")

# Supprimer les lignes sans titre pertinent (exemple: 'Results' ou lignes vides)
df = df[df['titre'].str.strip() != ""]
df = df[~df['titre'].str.lower().str.contains("results")]

# Aperçu des données
print(f"Nombre de produits : {len(df)}")
print(df.head())

# Nettoyage et préparation des données

# Nettoyer la colonne 'prix' : enlever le symbole $ et convertir en float
df['prix_nettoye'] = df['prix'].str.replace(r'[^\d.,]', '', regex=True).str.replace(',', '').astype(float, errors='ignore')

# Nettoyer la colonne 'note' : extraire la note numérique (ex: '4.5 out of 5 stars' -> 4.5)
df['note_num'] = df['note'].str.extract(r'([\d,.]+)').replace(',', '.', regex=True).astype(float, errors='ignore')

# Nettoyer la colonne 'nb_avis' : enlever les virgules et convertir en float
df['nb_avis_num'] = pd.to_numeric(df['nb_avis'].str.replace(',', ''), errors='coerce')

# Statistiques descriptives
print("\nStatistiques descriptives des prix :")
print(df['prix_nettoye'].describe())

print("\nStatistiques descriptives des notes :")
print(df['note_num'].describe())

print("\nStatistiques descriptives du nombre d'avis :")
print(df['nb_avis_num'].describe())

# Visualisations

# Histogramme des prix
plt.figure(figsize=(8,5))
sns.histplot(df['prix_nettoye'].dropna(), bins=30, kde=True)
plt.title("Distribution des prix des produits")
plt.xlabel("Prix (USD)")
plt.ylabel("Nombre de produits")
plt.show()

# Histogramme des notes
plt.figure(figsize=(8,5))
sns.countplot(x='note_num', data=df)
plt.title("Distribution des notes des produits")
plt.xlabel("Note")
plt.ylabel("Nombre de produits")
plt.show()

# Histogramme du nombre d'avis (log scale pour mieux visualiser)
plt.figure(figsize=(8,5))
sns.histplot(np.log1p(df['nb_avis_num'].dropna()), bins=30, kde=True)
plt.title("Distribution logarithmique du nombre d'avis")
plt.xlabel("Log(1 + nombre d'avis)")
plt.ylabel("Nombre de produits")
plt.show()

# Relation prix vs note
plt.figure(figsize=(8,5))
sns.scatterplot(x='prix_nettoye', y='note_num', data=df)
plt.title("Note en fonction du prix")
plt.xlabel("Prix (USD)")
plt.ylabel("Note")
plt.show()

# Relation note vs nombre d'avis (échelle logarithmique sur y)
plt.figure(figsize=(8,5))
sns.boxplot(x='note_num', y='nb_avis_num', data=df)
plt.title("Nombre d'avis en fonction de la note")
plt.xlabel("Note")
plt.ylabel("Nombre d'avis")
plt.yscale('log')
plt.show()

# Longueur des titres (nombre de mots)
df['longueur_titre'] = df['titre'].apply(lambda x: len(str(x).split()))

plt.figure(figsize=(8,5))
sns.histplot(df['longueur_titre'], bins=20, kde=True)
plt.title("Distribution de la longueur des titres")
plt.xlabel("Nombre de mots dans le titre")
plt.ylabel("Nombre de produits")
plt.show()
