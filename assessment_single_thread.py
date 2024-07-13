import requests
import time
import csv
from bs4 import BeautifulSoup

# global headers to be used for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

def extract_movie_details(movie_link):
    time.sleep(0.1)  # Espera curta para simular um pequeno atraso
    response = requests.get(movie_link, headers=headers)
    movie_soup = BeautifulSoup(response.content, 'html.parser')

    if movie_soup is not None:
        title = None
        date = None
        rating = None
        plot_text = None

        # Encontrando a seção específica
        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})
        
        if page_section is not None:
            # Encontrando todas as divs dentro da seção
            divs = page_section.find_all('div', recursive=False)
            
            if len(divs) > 1:
                target_div = divs[1]
                
                # Encontrando o título do filme
                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()
                
                # Encontrando a data de lançamento
                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()
                
                # Encontrando a classificação do filme
                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                if rating_tag:
                    rating = rating_tag.get_text()
                
                # Encontrando a sinopse do filme
                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                if plot_tag:
                    plot_text = plot_tag.get_text().strip()
                
                with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                    movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if all([title, date, rating, plot_text]):
                        print(title, date, rating, plot_text)
                        movie_writer.writerow([title, date, rating, plot_text])

def extract_movies(soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    for movie_link in movie_links:
        extract_movie_details(movie_link)

def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)

if __name__ == '__main__':
    main()
