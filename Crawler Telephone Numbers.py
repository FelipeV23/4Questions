import requests
from bs4 import BeautifulSoup


domain = "https://django-anuncios.solyd.com.br"
url_cars  = "https://django-anuncios.solyd.com.br/automoveis/"


def request(url):
    try:
        answer = requests.get(url)
        if  answer.status_code == 200:
            return answer.text
    except Exception as error:
        print(error)


def parsing(answer):
    try:
        soup = BeautifulSoup(answer, "html.parser")
        return soup
    except Exception as error:
        print("Error")
        print(error)


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


def acess_announcement(link):
    try:
        announcement = requests.get(domain + link)
        if announcement.status_code == 200:
            return announcement
    except Exception as error:
        print(error)


def search_telephone(soup):
    if soup:
        div_primary = soup.find_all("div", class_="sixteen wide column")
        if div_primary:
            div_secondary = div_primary.find("h3", class_="ui dividing header")
            print(div_secondary)


answer = request(url_cars)
if answer:
    soup = parsing(answer)
    if soup:
        links = search_cars(soup)
        if links:
            answer_link = request(domain + links[2])
            if answer_link:
                soup2 = parsing(answer_link)
                if soup2:
                    search_telephone(soup2)

