import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from errorhandle import *
from time import sleep
from database import *
from os import path

cwd = os.getcwd()
chrome_driver_file = (path.join(os.getcwd(), "storage", "chromedriver.exe"))
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2,
                                                    'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                    'media_stream_mic': 2, 'media_stream_camera': 2,
                                                    'protocol_handlers': 2,
                                                    'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                    'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop': 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement': 2,
                                                    'durable_storage': 2}}

options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('window-size=1920x1080')
options.add_argument(('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'))


def open_driver():
    try:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        driver.maximize_window()

        return driver
    except Exception as e:
        # print("error", e)
        return {"success": False, "error": e}


def close_driver(driver):
    driver.quit()
    return {"success": True}


def multi_list(link_list_number):
    links = search_for_link()["data"]
    links_length = len(links)
    if links_length == 0:
        return False
    else:
        result = links_length / link_list_number
        divideNum = int(result)
        mod = links_length % link_list_number
        a_list = []
        extra = False
        for i in range(link_list_number):
            list_of_list = []
            if i < mod:
                divideNum += 1
                extra = True
            for j in links[:divideNum]:
                list_of_list.append(j)
            del links[:divideNum]
            a_list.append(list_of_list)
            if extra:
                divideNum -= 1
                extra = False
        return {"success": True,"data":a_list}

def search_for_link():
    link_list = []
    try:
        all_objects = Links.objects(websiteName="www.publicstorage.com")
        for obj in all_objects:
            link_list.append(obj.link)
            # print(obj.link)
        return {"success": True, "data": link_list}
    except Exception as e:
        print(e)


# search_for_link()


def check_items(driver, _id):
    try:
        item_size = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,
                                            """//h4[contains(text(),"Medium 10' x 10'")]"""))).text
        # print(item_size)
    except:
        print("No item found")
        item_size = False
    if item_size == "Medium 10' x 10'":

        try:
            path = """//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//child::li//child::span[contains(text(),"Inside unit")]//parent::li/preceding-sibling::li//child::span[contains(text(),"Climate Controlled")]"""
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, path)))

            result = "inside_unit_climate_control"
        except:
            try:
                iu_path = """//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//child::li//child::span[contains(text(),"Inside unit")]"""
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, iu_path)))

                result = "inside_unit"

            except:
                try:
                    path = """(//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//li//child::span[contains(text(),"Climate Controlled")])[1]"""

                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, path)))
                    result = "outside_unit_climate_control"
                except:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        """(//h4[contains(text(),"Medium 10' x 10'")])[1]""")))

                    result = "outside_unit"
        size = item_size.replace("Medium ", "")
        print("size: ", size)

        if result == "inside_unit_climate_control":
            price_path = """(//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//child::li//child::span[contains(text(),"Inside unit")]//parent::li/preceding-sibling::li//child::span[contains(text(),"Climate Controlled")]//parent::li//parent::ul//parent::div/following-sibling::div/div/div/span/span)[1]"""
            price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            print("climate_control: ", True)
            print("price: ", price)
            push_records(_id, size, True, float(price))
        elif result == "inside_unit":

            price_path = """(//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//child::li//child::span[contains(text(),"Inside unit")]//parent::li//parent::li//parent::ul//parent::div/following-sibling::div/div/div/span/span)[1]"""
            price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            print("climate_control: ", False)
            print("price", price)
            push_records(_id, size, False, float(price))
        elif result == "outside_unit_climate_control":
            price_path = """(//h4[contains(text(),"Medium 10' x 10'")]/following-sibling::ul//li//child::span[contains(text(),"Climate Controlled")]//parent::li//parent::ul//parent::div/following-sibling::div/div/div/span/span)[1]"""
            price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            print("climate_control: ", True)
            print("price: ", price)
            push_records(_id, size, True, float(price))
        else:
            price_path = """(//h4[contains(text(),"Medium 10' x 10'")]//parent::div/following-sibling::div/div/div/span/span)[1]"""
            price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            print("climate_control: ",False)
            print("price: ", price)
            push_records(_id, size, False, float(price))

    else:
        pass


def runBot(links_list):
    driver = open_driver()
    for link in links_list:
        driver.get(link)
        objcts = Links.objects.get(link=link)
        owner_id = objcts.id
        print("link: ", link)
        check_items(driver, owner_id)
        print("======================data===========================")
    close_driver(driver)
