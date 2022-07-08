from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd



url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = bs(response.text, 'lxml')

movies = soup.select("td.titleColumn")
link = soup.select('td.titleColumn a')
links =[a.attrs.get('href') for a in link]
crew = soup.select('td.titleColumn a')
crews = [a.attrs.get('title') for a in crew]
rating = soup.select("td.posterColumn span[name=ir]")
ratings = [b.attrs.get('data-value') for b in rating]
vote = soup.select("td.ratingColumn strong")
votes = [b.attrs.get('data-value') for b in vote]



imdb = []

for index in range(0,len(movies)):
    movie_string = movies[index].get_text()
    movie = (' ').join(movie_string.split()).replace('.',',') # 100, cadena perpetua (1994)
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]

    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": crews[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    
    imdb.append(data)

df = pd.DataFrame(imdb)

df.to_csv('top_250_movies.csv')