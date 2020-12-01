import requests
import csv
from bs4 import BeautifulSoup

URL_BEAUTYONWHEELS_AVENE = 'https://beautyonwheels.ae/collections/avene'
URL_BASHACARE_AVENE =  'https://www.basharacare.com/ae_en/avene?p=1'
URL_BASHACARE_FILORGA = 'https://www.basharacare.com/ae_en/filorga?p=1'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
}

def get_html(url, params=''):
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def save_csv(products):
    with open('Products.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Product name', 'Price'])
        for item in products:
            writer.writerow([item['Product_name'], item['Price_']])

def get_content_beautyonwheels_avene(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ProductItem__Wrapper')
    products = []

    for item in items:
        products.append({
            'Product_name': 'Avene ' + item.find('h2', class_='ProductItem__Title Heading').get_text(strip=True),
            'Price_': item.find('span', class_='money').get_text(strip=True)
        })
    return products

def get_content_basharacare_avene_filorga(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product details product-item-details')
    products = []

    for item in items:
        price = item.find('span', class_='price-final_price').find('span', class_='price')

        products.append({
            'Product_name': 'Avene ' + item.find('a', class_='product-item-link').get_text(strip=True),
            'Price_': price.get_text(strip=True) + ' AED'
        })
    return products

def parser():
    products = []
    HTML_BEAUTYONWHEELS_AVENE = get_html(URL_BEAUTYONWHEELS_AVENE)
    products.extend(get_content_beautyonwheels_avene(HTML_BEAUTYONWHEELS_AVENE.text))

    for page in range(1, 3):
        HTML_BASHACARE_AVENE = get_html(URL_BASHACARE_AVENE, params={'p': page})
        products.extend(get_content_basharacare_avene_filorga(HTML_BASHACARE_AVENE.text))
        HTML_BASHACARE_FILORGA = get_html(URL_BASHACARE_FILORGA, params={'p': page})
        products.extend(get_content_basharacare_avene_filorga(HTML_BASHACARE_FILORGA.text))

    save_csv(products)

parser()