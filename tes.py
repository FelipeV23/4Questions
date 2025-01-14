import requests
from bs4 import BeautifulSoup

domain = "https://django-anuncios.solyd.com.br"
url_cars = "https://django-anuncios.solyd.com.br/automoveis/"

def request(url):
    try:
        answer = requests.get(url)
        if answer.status_code == 200:
            return answer.text
    except Exception as error:
        print(error)
        return None

def parsing(answer):
    try:
        soup = BeautifulSoup(answer, "html.parser")
        return soup
    except Exception as error:
        print("Error in parsing")
        print(error)
        return None

def search_cars(soup):
    if soup:
        div_primary = soup.find("div", class_="ui three doubling link cards")
        if div_primary:
            div_secondary = div_primary.find_all("a", class_="card")
            cars_list = []
            for cars in div_secondary:
                link_car = cars["href"]
                cars_list.append(link_car)
            return cars_list
    return []

def acess_announcement(link):
    try:
        announcement = requests.get(domain + link)
        if announcement.status_code == 200:
            return announcement
    except Exception as error:
        print(error)
        return None

def search_telephone(soup):
    div_primary = soup.find_all("div", class_="sixteen wide column")
    if div_primary:
        for div in div_primary:
            print(div.get_text())  # Imprime o conteúdo da div
    else:
        print("No content found in the div.")

# Fluxo principal
answer = request(url_cars)
if answer:
    soup = parsing(answer)
    if soup:
        links = search_cars(soup)
        if links:
            print("Links encontrados:", links)
            answer_link = request(domain + links[1])  # Passando a URL correta
            if answer_link:
                soup2 = parsing(answer_link)
                if soup2:
                    search_telephone(soup2)
