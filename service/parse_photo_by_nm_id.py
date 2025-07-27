from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import requests
from PIL import Image
import io
import os 
import shutil

async def parse_photos(list_of_nm_ids: list):
    options = Options()
    options.add_argument("--disable-gpu")

    shutil.rmtree("images")
    os.makedirs("images")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    for index, nm_id in enumerate(list_of_nm_ids):
        driver.get(f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx")

        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//img[@data-link="{on \'load\' ~onImgLoad}"]')
            )
        )
        img_url = img_element.get_attribute('src') # or img_element.get_attribute('data-src-pb')

        # print("URL изображения:", img_url)

        # img_url = "https://nsk-basket-cdn-08.geobasket.ru/vol1623/part162318/162318319/images/big/1.webp"
        response = requests.get(img_url)
        if response.status_code == 200:
            webp_image = Image.open(io.BytesIO(response.content))
            webp_image.convert("RGB").save(f"images/image_{index}.jpg", "JPEG", quality=100)
        
            # with open(f'images/wildberries_image_{index}.webp', 'wb') as f:
            #     f.write(response.content)
            print("Фото успешно сохранено!")
        else:
            print("Ошибка загрузки:", response.status_code)

    driver.quit()
