import requests
from bs4 import BeautifulSoup
import time
from lxml.etree import tostring
from lxml.builder import E

page_number = 1


def print_annonce_details(date_heure, url, price, id_publication, marque, etat, transmission, modele,
                          kilometrage, carburant, carosserie):
    print("date et heure de publication : " + str(date_heure) + "\n")
    print("url : " + str(url) + "\n")
    print("price : " + str(price) + "\n")
    print("id_publication : " + str(id_publication) + "\n")
    print("marque : " + str(marque) + "\n")
    print("etat : " + str(etat) + "\n")
    print("transmission : " + str(transmission) + "\n")
    print("modele : " + str(modele) + "\n")
    print("kilometrage : " + str(kilometrage) + "\n")
    print("carburant : " + str(carburant) + "\n")
    print("carosserie : " + str(carosserie) + "\n")
    print("=========== END ANNONCE ===========\n ")



def find_description(index, soup_page_annonce):
    try:
        value = soup_page_annonce.select('.listing-item__properties__description')[index].text
    except:
        value="aucun"
    return value



def scrap_expat_dakar():
    for i in range(10):
        print(" Page : " + str(i + 1))
        page = requests.get('https://www.expat-dakar.com/voitures/dakar?page=' + str(i + 1))
        soup = BeautifulSoup(page.content, 'html.parser')
        listings = soup.select('.listings-cards__list-item')
        for annonce in listings:
            href = annonce.a["href"]
            page_annonce = requests.get(href)
            soup_page_annonce = BeautifulSoup(page_annonce.content, 'html.parser')
            date_heure = soup_page_annonce.select('.listing-item__details__date')
            price = soup_page_annonce.select('.listing-card__price__value')
            id_publication = soup_page_annonce.select('.listing-item__details__ad-id')
            marque = find_description(0, soup_page_annonce)
            etat = find_description(1, soup_page_annonce)
            transmission = find_description(2, soup_page_annonce)
            modele = find_description(3, soup_page_annonce)
            kilometrage = find_description(4, soup_page_annonce)
            carburant = find_description(5, soup_page_annonce)
            carosserie = find_description(6, soup_page_annonce)
            print_annonce_details(date_heure, href, price, id_publication, marque, etat, transmission, modele,
                                  kilometrage, carburant, carosserie)
        time.sleep(6)



def create_xml_file():
    value = tostring(
        E.results(
            E.Country(name='Germany',
                      Code='DE',
                      Storage='Basic',
                      Status='Fresh',
                      Type='Photo')
        ), pretty_print=True, xml_declaration=True, encoding='UTF-8')
    text = soup = BeautifulSoup(value, 'xml')
    print(text)
    f = open("file.xml", "w")
    f.write(str(text))
    f.close()

scrap_expat_dakar()
#create_xml_file()







