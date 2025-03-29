import time
import os
import requests
import zipfile
import configparser
import re

from web_scraper.utils.driverOptions import options as chrome_options
from selenium import webdriver
from selenium.webdriver.common.by import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TODO Melhor os loggins e as referencias dos elementos fazer um arquivo na pastas utils

class Crawler:
    def __init__(self):

        self.config = self.load_config()
        self.url = self.config["SELENIUM"]["url"]
        self.download_dir = self.config["SELENIUM"]["download_dir"]

        try:

            self.accessing_url()
            self.start_download_annex_1()
            self.start_download_annex_2()
            print("Finalizando")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

        finally:
            print("Fechando tudo")
            self.driver.quit()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read("C:\\repo\\intuitive_care\\.config")
        return config

    def accessing_url(self):

        try:

            self.open_driver()
            self.driver.get(self.url)
            time.sleep(3)
            cookie_button = self.driver.find_element(By.CSS_SELECTOR, "body > div.dsgov > div > div > div > div > "
                                                                      "div.br-modal-footer.actions > button.br-button"
                                                                      ".secondary.small.btn-accept")

            cookie_button.click()


        except Exception as e:

            print(f"Ocorreu um erro: {e}")
            self.driver.quit()

    def start_download_annex_1(self):

        try:

            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.driver.find_element(By.CSS_SELECTOR, "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(1) > a:nth-child(1)")))
            download_annex = self.driver.find_element(By.CSS_SELECTOR, "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(1) > a:nth-child(1)")
            download_annex.click()

            time.sleep(5)
            self.switch_window()
            self.request_pdf()
            self.close_window()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

    def start_download_annex_2(self):

        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.driver.find_element(By.CSS_SELECTOR,
                                                                                                    "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(1) > a:nth-child(1)")))
            download_annex = self.driver.find_element(By.CSS_SELECTOR,
                                                        "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(2) > a")
            download_annex.click()

            time.sleep(5)
            self.switch_window()
            self.request_pdf()
            self.close_window()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()


    def open_driver(self):

        try:

            self.driver = webdriver.Chrome(options=chrome_options)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

    def close_driver(self):
        self.driver.close()

    def switch_window(self):

        try:

            handles = self.driver.window_handles
            for handle in handles:

                self.driver.switch_to.window(handle)

                url = self.driver.current_url

                if "Anexo" in url:

                    print(f"Found PDF: {os.path.basename(url)}")
                    self.pdf_title = os.path.basename(url)
                    break


            return self.pdf_title

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

    def close_window(self):

        try:

            handles = self.driver.window_handles

            self.driver.switch_to.window(handles[1])
            self.driver.close()
            self.driver.switch_to.window(handles[0])

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

    def request_pdf(self):
        try:
            download_dir = self.config["SELENIUM"]["download_dir"]
            self.create_dowload_dir()

            url = self.driver.current_url
            response = requests.get(url)

            file_downloaded = os.path.join(download_dir, self.pdf_title)

            if response.status_code == 200:
                with open(file_downloaded, "wb") as file:
                    file.write(response.content)

                match = re.match(r"([A-Za-z]+_[A-Za-z]+)", self.pdf_title)
                file_name = match.group(0)
                file_name = file_name[0].lower() + file_name[1:]

                zip_file = os.path.join(download_dir, file_name + ".zip")

                with zipfile.ZipFile(zip_file, "w") as zipf:
                    for file_name in os.listdir(download_dir):
                        file_path = os.path.join(download_dir, file_name)
                        if os.path.isfile(file_path) and not file_name.endswith(".zip"):
                            zipf.write(file_path, os.path.basename(file_path))

                if os.path.exists(file_downloaded):
                    os.remove(file_downloaded)

                print("Download and compression completed successfully!")
            else:
                print(f"Error downloading: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

    def create_dowload_dir(self):
        try:
            download_dir =  self.download_dir
            os.makedirs(download_dir, exist_ok=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()

crawler = Crawler()
