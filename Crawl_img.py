import os
import requests
from bs4 import BeautifulSoup
import time
class CarImageScraper:
    def __init__(self):
        self.base_url = 'https://www.bobaedream.co.kr/cyber/CyberCar.php?sel_m_gubun=ALL&order=S11&view_size=70&page'
        self.image_directory = 'img3'
                
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)

    def scrape_images(self, start_page=1, end_page=10):
        for page_number in range(start_page, end_page + 1):
            url = f'{self.base_url}={page_number}'
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            
            for link in soup.select('.list-inner .img'):
                 
                 if link.has_attr('href'):
                     
                    urlLink = 'https://www.bobaedream.co.kr/'+link['href']
                    res1 = requests.get(urlLink)
                    soup1 = BeautifulSoup(res1.content, 'html.parser')

                    car_titles1 = soup1.select('h3.tit')
                    car_titles2 = soup1.select('.tbl-01.st-low tbody>tr:first-child th:first-child+td')
                    content = (car_titles1[0].text.strip() + car_titles2[0].text.strip())
                    renamed_title = content.replace('  ','_').replace(' ', '_').replace('-', '').replace('.', '~')            
                    directory_name = os.path.join(self.image_directory, renamed_title)
                    car_images1 = soup1.select('.gallery a')
                    href = car_images1
                    for image in car_images1:
                        href = image['href']

                        if not os.path.exists(directory_name):
                            os.makedirs(directory_name)

                        image_urlLink = "https:"+href

                        image_data = requests.get(image_urlLink).content
                        image_path = os.path.join(directory_name, str(time.time()) + ".png")

                        with open(image_path, 'wb') as img_file:
                            img_file.write(image_data)

                        print(f'Saved {renamed_title}/image.jpg') 

scraper = CarImageScraper()
scraper.scrape_images(start_page=1, end_page=3)

