# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.5",
# }

# URL = 'https://www.amazon.com/s?k=playstation+5'

# response = requests.get(URL, headers=HEADERS)
# soup = BeautifulSoup(response.content, 'html.parser')

# # Listes vides
# titles, prices, ratings, reviews = [], [], [], []

# # Tous les blocs produits
# for product in soup.select("div.s-main-slot div.s-result-item"):

#     # Titre
#     title = product.h2.get_text(strip=True) if product.h2 else ""
#     titles.append(title)

#     # Prix
#     price_whole = product.select_one("span.a-price > span.a-offscreen")
#     prices.append(price_whole.get_text(strip=True) if price_whole else "")

#     # Note
#     rating = product.select_one("span.a-icon-alt")
#     ratings.append(rating.get_text(strip=True) if rating else "")

#     # Nombre d’avis
#     review = product.select_one("span.a-size-base")
#     reviews.append(review.get_text(strip=True) if review else "")

# # Créer le DataFrame
# df = pd.DataFrame({
#     "titre": titles,
#     "prix": prices,
#     "note": ratings,
#     "nb_avis": reviews
# })

# # Supprimer les lignes sans titre
# df = df[df["titre"] != ""]

# # Enregistrer
# df.to_csv("amazon_resultats.csv", index=False)
# print(df.head())

# import pandas as pd
# import numpy as np

# df = pd.read_csv("avis_nettoyes.csv")

# # Générer aléatoirement 0 ou 1 (à remplacer plus tard par tes vrais labels)
# df["label"] = np.random.randint(0, 2, size=len(df))

# df.to_csv("avis_labellises.csv", index=False)
# print(df[["titre_nettoye", "label"]].head())




import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

# Nombre de pages que tu veux scraper
NB_PAGES = 10  # ⇦ tu peux augmenter ce nombre (max 20 recommandé sans proxy)

# Recherche sur Amazon
BASE_URL = "https://www.amazon.com/s?k=wireless+headphones&i=electronics&page="


# Listes vides pour stocker les résultats
titles, prices, ratings, reviews = [], [], [], []

for page in range(1, NB_PAGES + 1):
    print(f" Scraping page {page}...")
    url = BASE_URL + str(page)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    for product in soup.select("div.s-main-slot div.s-result-item"):
        # Titre
        title = product.h2.get_text(strip=True) if product.h2 else ""
        titles.append(title)

        # Prix
        price = product.select_one("span.a-price > span.a-offscreen")
        prices.append(price.get_text(strip=True) if price else "")

        # Note
        rating = product.select_one("span.a-icon-alt")
        ratings.append(rating.get_text(strip=True) if rating else "")

        # Nombre d’avis
        review = product.select_one("span.a-size-base")
        reviews.append(review.get_text(strip=True) if review else "")

    time.sleep(2)  # Pause pour ne pas se faire bloquer

# Créer le DataFrame
df = pd.DataFrame({
    "titre": titles,
    "prix": prices,
    "note": ratings,
    "nb_avis": reviews
})

# Nettoyage : supprimer les lignes sans titre
df = df[df["titre"] != ""]

# Enregistrer les résultats
df.to_csv("amazon_resultats.csv", index=False)
print(f"\n Scraping terminé : {len(df)} produits enregistrés dans 'amazon_resultats.csv'")
print(df.head())
