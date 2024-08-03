import requests
from bs4 import BeautifulSoup
import time
from lxml.etree import tostring
from lxml import etree
from lxml.builder import E


def print_annonce_details(date_heure, url, price, id_publication, marque, etat, transmission, modele,
                          kilometrage, carburant, carosserie, image):
    array = date_heure.split(",")
    dic = {
        "date" : array[0],
        "heure": array[1],
        "url": url,
        "prix": price,
        "id_publication":id_publication,
        "marque" : marque,
        "etat": etat,
        "transmission": transmission,
        "modele" : modele,
        "kilometrage": kilometrage,
        "carburant" : carburant,
        "carrosserie" : carosserie,
        "image" : image,
    }
    #print(dic)
    return dic



def find_description(index, soup_page_annonce):
    try:
        value = soup_page_annonce.select('.listing-item__properties__description')[index].text
    except:
        value = "aucun"
    return value


def find(soup, class_name):
    try:
        value = soup.select(class_name)[0].text
    except:
        value = "aucun"
    return value


def scrap_image(soup, class_name):
    try:
        value = soup.select(class_name)[0].get('src')
    except:
        value = "aucun"
    return value



def scrap_expat_dakar():
    count = 0
    annonces = []
    for i in range(50):
        number_page = i+1
        print("Scraping Page : https://www.expat-dakar.com/voitures/dakar?page=" + str(number_page))
        page = requests.get('https://www.expat-dakar.com/voitures/dakar?page=' + str(number_page))
        soup = BeautifulSoup(page.content, 'html.parser')
        listings = soup.select('.listings-cards__list-item')
        for annonce in listings:
            href = annonce.a["href"]
            page_annonce = requests.get(href)
            soup_page_annonce = BeautifulSoup(page_annonce.content, 'html.parser')
            date_heure = find(soup_page_annonce,'.listing-item__details__date')
            price = find(soup_page_annonce,'.listing-card__price__value')
            id_publication = find(soup_page_annonce, '.listing-item__details__ad-id')
            image = scrap_image(soup_page_annonce, '.gallery__image__resource')
            marque = find_description(0, soup_page_annonce)
            etat = find_description(1, soup_page_annonce)
            transmission = find_description(2, soup_page_annonce)
            modele = find_description(3, soup_page_annonce)
            kilometrage = find_description(4, soup_page_annonce)
            carburant = find_description(5, soup_page_annonce)
            carosserie = find_description(6, soup_page_annonce)
            dic = print_annonce_details(date_heure, href, price, id_publication, marque, etat, transmission, modele,
                                  kilometrage, carburant, carosserie, image)
            annonces.append(dic)
            count += 1
        time.sleep(10)

    print(" Total : " + str(count))
    return annonces



def create_xml_file(array_of_annonce):
    print("Writing in xml file...")
    publications = etree.Element("publications")
    for index in range(len(array_of_annonce)):
        pub = etree.Element("pub")
        pub.set("id", array_of_annonce[index]["id_publication"].strip())
        pub.set("date", array_of_annonce[index]["date"].strip())
        pub.set("heure", array_of_annonce[index]["heure"].strip())

        image = etree.Element("Image", src=array_of_annonce[index]['image'])
        url = etree.Element("Url")
        url.text = array_of_annonce[index]['url']
        prix = etree.Element("Prix")
        prix.text = array_of_annonce[index]['prix']
        marque = etree.Element("Marque")
        marque.text = array_of_annonce[index]['marque']
        modele = etree.Element("Modele")
        modele.text = array_of_annonce[index]['modele']
        transmission = etree.Element("Transmission")
        transmission.text = array_of_annonce[index]["transmission"]
        kilometrage = etree.Element("kilometrage")
        kilometrage.text = array_of_annonce[index]["kilometrage"]
        carburant = etree.Element("carburant")
        carburant.text = array_of_annonce[index]["carburant"]
        carrosserie = etree.Element("carrosserie")
        carrosserie.text = array_of_annonce[index]["carrosserie"]
        pub.append(image)
        pub.append(url)
        pub.append(prix)
        pub.append(marque)
        pub.append(modele)
        pub.append(kilometrage)
        pub.append(carburant)
        pub.append(carrosserie)
        publications.append(pub)
    value = tostring(publications, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    text = BeautifulSoup(value, 'xml')
    #print(text)
    f = open("file.xml", "w")
    f.write(str(text))
    f.close()

annonces = scrap_expat_dakar()
create_xml_file(annonces)







