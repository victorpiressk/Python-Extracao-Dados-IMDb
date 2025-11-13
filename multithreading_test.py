import requests
import time
import csv
import random
import concurrent.futures


from bs4 import BeautifulSoup

# global headers to be used for requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

MAX_THREADS = 10


def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = BeautifulSoup(requests.get(movie_link, headers=headers).content, 'html.parser')
    movie_soup = response

    if movie_soup is not None:
        title = None
        date = None

        movie_data = movie_soup.find('div', attrs={'class': 'title_wrapper'})
        if movie_data is not None:
            title = movie_data.find('span', class_="hero__primary-text").get_text()
            date = movie_data.find('a', attrs={'title': 'See more release dates'}).get_text().strip()

        rating = movie_soup.find('span', attrs={'itemprop': 'ratingValue'}).get_text() if movie_soup.find(
            'span', attrs={'itemprop': 'ratingValue'}) else None

        plot_text = movie_soup.find('div', attrs={'class': 'summary_text'}).get_text().strip() if movie_soup.find(
            'div', attrs={'class': 'summary_text'}) else None

        with open('movies.csv', mode='a') as file:
            movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if all([title, date, rating, plot_text]):
                print(title, date, rating, plot_text)
                movie_writer.writerow([title, date, rating, plot_text])


# def extract_movies(soup):
#     movies_list = soup.find('div', class_='sc-3196e3ca-3').find('ul')
#     movies_list_item = movies_list.find_all('li')
#     movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_list_item]

#     threads = min(MAX_THREADS, len(movie_links))
#     with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#         executor.map(extract_movie_details, movie_links)

# def extract_movies(soup):
#     # A nova página do IMDb usa <li> para listar os filmes
#     movies_list = soup.find_all('li', class_='ipc-metadata-list-summary-item')

#     movie_links = []
#     for movie in movies_list:
#         link_tag = movie.find('a', href=True)
#         if link_tag and '/title/' in link_tag['href']:
#             movie_links.append('https://www.imdb.com' + link_tag['href'])

#     print(f"{len(movie_links)} filmes encontrados.")

#     threads = min(MAX_THREADS, len(movie_links))
#     with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#         executor.map(extract_movie_details, movie_links)

def extract_movies(soup):
    # Extrai os links dos filmes da página de 'Most Popular Movies' do IMDb
    # e executa a coleta de dados em paralelo usando threads.

    # movies_list = soup.find('ul')
    # movies_items = movies_list.find_all('li', class_='ipc-metadata-list-summary-item')

    movies_list = soup.find_all('li', class_='ipc-metadata-list-summary-item')

    # Encontra o <a> dentro da hierarquia de cada li (mesmo que esteja dentro de um div > img)
    movie_links = []
    for movie in movies_list:
        a_tag = movie.find('a', href=True)
        if a_tag and a_tag['href'].startswith('/title/'):
            movie_links.append('https://imdb.com' + a_tag['href'])

    print(f"{len(movie_links)} filmes encontrados.")

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)


def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/pt/chart/moviemeter/?ref_=hm_nv_menu'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)


if __name__ == '__main__':
    main()