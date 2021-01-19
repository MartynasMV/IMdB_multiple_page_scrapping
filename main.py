import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint

titles = []
years = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

headers = {"Accept-Language": "en-US, en; q=0.5"}

pages = np.arange(1,101,50)
url = 'https://www.imdb.com/search/title/?groups=top_1000&start='
for page in pages:
    page = requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    sleep(randint(2,10))
    for container in movie_div:
        title_raw = container.h3.a.text
        titles.append(title_raw)
        year_raw = container.find('span', class_='lister-item-year').text
        years.append(year_raw)
        imdb_ratings_raw = container.find('div', class_='ratings-bar').strong.text
        imdb_ratings.append(imdb_ratings_raw)
        metascores_raw = container.find('div', class_='ratings-metascore').span.text if container.find('div', class_='ratings-metascore').span.text else '-'
        metascores.append(metascores_raw)
        votes_and_gross = container.find_all('span', attrs={'name':'nv'})
        votes_raw = votes_and_gross[0].text
        votes.append(votes_raw)
        us_gross_raw = votes_and_gross[1].text if len(votes_and_gross)>1 else "-"
        us_gross.append(us_gross_raw)

movies = pd.DataFrame({
    "Movie": titles,
    "Year" : years,
    "IMdB rating" : imdb_ratings,
    "Metascore" : metascores,
    "Total Votes" : votes,
    "Gross_USA_Millions" : us_gross,
})
#print(movies.dtypes)
#print(movies)
#Cleaning:

movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['IMdB rating'] = movies['IMdB rating'].str.extract('(\d+)').astype(int)
movies['Metascore'] = movies['Metascore'].str.extract('(\d+)')
movies['Metascore'] = pd.to_numeric(movies['Metascore'], errors='coerce')
movies['Total Votes'] = movies['Total Votes'].str.replace(',','').astype(int)
movies['Gross_USA_Millions'] = movies['Gross_USA_Millions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['Gross_USA_Millions'] = pd.to_numeric(movies['Gross_USA_Millions'], errors='coerce')

#check empty data responses:
#print(movies.isnull().sum())
#return if no data:
movies.Gross_USA_Millions = movies.Gross_USA_Millions.fillna("")
movies.Metascore = movies.Metascore.fillna("None Given")

print(movies)
#print(movies.to_csv('movies.csv'))


