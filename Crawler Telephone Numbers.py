import re
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


DOMAIN = "https://django-anuncios.solyd.com.br"
URL_CARS  = "https://django-anuncios.solyd.com.br/automoveis/"
TELEPHONES = []


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
        try:
            div_primary = soup.find("div", class_="ui three doubling link cards")
            if div_primary:
                div_secondary = div_primary.find_all("a", class_="card")
                cars_list = []
                for cars in div_secondary:
                    link_car = cars["href"]
                    cars_list.append(link_car)
                return cars_list
        except Exception as error:
            print(error)
            return None


def search_telephone(soup):
    if soup:
        try:
            div_primary = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
        except Exception as error:
            print(error)
            return None
    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", div_primary)
    if regex:
        return regex


def find_out_telephones(links):

    answer_announcement = request(DOMAIN + links)

    if answer_announcement:
        soup = parsing(answer_announcement)
        if soup:
            telephones = search_telephone(soup)
            if telephones:
                for telephone in telephones:
                    TELEPHONES.append(telephone)
                    telephone = ''.join(telephone)
                    print("Telephone finding:", telephone)
                    save_telephones(telephone)


def save_telephones(telephone):
        try:
            with open("database.csv", "a") as file:
                file.write(str(telephone + "\n"))
        except Exception as error:
            print(error)


if __name__ == "__main__":
    answer = request(URL_CARS)
    if answer:
        soup = parsing(answer)
        if soup:
            links = search_cars(soup)
            if links:
                with ThreadPoolExecutor(max_workers=7) as executor:
                    executor.map(find_out_telephones, links)

