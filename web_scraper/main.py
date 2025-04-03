import time
import os
import requests
import zipfile
import configparser
import re
import json

from web_scraper.utils.selenium_elements import *
from web_scraper.utils.driver_options import options as chrome_options
from selenium import webdriver
from pdf_reader.pdf_to_csv import PdfToCSV

#TODO Melhor os loggins

class WebScraper:
    def __init__(self):

        self.config = self.load_config()
        self.url = self.config["SELENIUM"]["url"]
        self.download_dir = self.config["SELENIUM"]["download_dir"]
        self.driver = self.config["SELENIUM"]["path"]
        self.accounting_folder = self.config["SELENIUM"]["accounting_folder"]
        self.operator_plans_folder = self.config["SELENIUM"]["operator_plans_folder"]
        self.accounting_url = self.config["SELENIUM"]["accounting_url"]
        self.operator_plan_url = self.config["SELENIUM"]["operator_plan_url"]
        self.cookies_folder = self.config["SELENIUM"]["cookies_folder"]
        self.extension_zip = self.config["EXTENSION"]["zip"]
        self.extension_pdf = self.config["EXTENSION"]["pdf"]
        self.extension_csv = self.config["EXTENSION"]["csv"]

        try:

            self.open_driver()
            self.accessing_url()
            self.start_download_annex_1()
            self.start_download_annex_2()
            self.accounting_year_1()
            self.accounting_year_2()
            self.operator_plans_download()
            print("Finishing")

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

        finally:
            self.driver.quit()

    @staticmethod
    def load_config():

        config = configparser.ConfigParser()
        config.read("C:\\repo\\intuitive_care\\.config")

        return config

    def accessing_url(self):

        try:

            time.sleep(3)
            self.driver.get(self.url)
            self.add_cookies()
            time.sleep(5)

            if self.cookies_load is False:
                self.save_cookies()

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def start_download_annex_1(self,):

        try:

            download_annex = self.driver.find_element(*download_annex_1)

            download_dir = self.download_dir
            self.create_folder_dir(download_dir)

            download_annex_url = download_annex.get_attribute("href")

            file_path = os.path.join(download_dir, os.path.basename(download_annex_url))
            response = requests.get(download_annex_url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def start_download_annex_2(self):

        try:

            download_annex = self.driver.find_element(*download_annex_2)

            download_dir = self.download_dir
            self.create_folder_dir(download_dir)

            download_annex_url = download_annex.get_attribute("href")

            file_path = os.path.join(download_dir, os.path.basename(download_annex_url))
            response = requests.get(download_annex_url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def accounting_year_1(self):

        try:

            extension_zip = self.extension_zip

            accounting_folder = self.accounting_folder
            self.create_folder_dir(accounting_folder)

            self.driver.get(self.accounting_url)
            accounting_files = self.driver.find_element(*accounting_files_e)

            accounting_url = accounting_files.get_attribute("href")
            self.driver.get(accounting_url)

            table_href = self.driver.find_element(*table_href_e)
            links = table_href.find_elements(*links_e)

            hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href").endswith(extension_zip)]

            for url in hrefs:

                time.sleep(3)
                file_downloaded = os.path.join(accounting_folder, os.path.basename(url))

                year_match = re.search(r"\d{4}", file_downloaded)
                if year_match:
                    final_folder = year_match.group()
                else:
                    continue

                folder_path = os.path.join(accounting_folder, final_folder)
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, os.path.basename(url))
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                time.sleep(3)
                self.extract_zip(file_path, folder_path)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def accounting_year_2(self):

        try:

            extension_zip = self.extension_zip

            accounting_folder = self.accounting_folder
            self.create_folder_dir(accounting_folder)

            self.driver.get(self.accounting_url)
            accounting_files = self.driver.find_element(*accounting_files_2_e)

            accounting_url = accounting_files.get_attribute("href")
            self.driver.get(accounting_url)

            table_href = self.driver.find_element(*table_href_e)
            links = table_href.find_elements(*links_e)

            hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href").endswith(extension_zip)]

            time.sleep(3)
            for url in hrefs:
                file_downloaded = os.path.join(accounting_folder, os.path.basename(url))

                year_match = re.search(r"\d{4}", file_downloaded)
                if year_match:
                    final_folder = year_match.group()
                else:
                    continue

                folder_path = os.path.join(accounting_folder, final_folder)
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, os.path.basename(url))
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                time.sleep(3)
                self.extract_zip(file_path, folder_path)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def operator_plans_download(self):

        try:

            extension_csv = self.extension_csv

            operator_plan_folder = self.operator_plans_folder
            self.create_folder_dir(operator_plan_folder)

            self.driver.get(self.operator_plan_url)

            table_href = self.driver.find_element(*table_href_e)
            links = table_href.find_elements(*links_e)

            hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href").endswith(extension_csv)]

            time.sleep(3)
            for url in hrefs:

                folder_path = operator_plan_folder
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, os.path.basename(url))

                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def open_driver(self):

        try:

            self.driver = webdriver.Chrome(options=chrome_options)

            self.driver.refresh()

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def close_driver(self):

        try:

            self.driver.close()

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def create_folder_dir(self,download_folder):

        try:

            download_dir =  download_folder
            os.makedirs(download_dir, exist_ok=True)

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def save_cookies(self):

        try:

            cookie_button = self.driver.find_element(*cokkies_button_e)
            cookie_button.click()

            cookies_path = os.path.join(self.cookies_folder, "cookies.json")
            cookies = self.driver.get_cookies()

            with open(cookies_path, "w") as file:
                json.dump(cookies, file)

        except Exception:
            print("No cookies yet!")

    def add_cookies(self):

        self.cookies_load = False

        try:
            cookies_path = os.path.join(self.cookies_folder, "cookies.json")

            with open(cookies_path, "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            self.cookies_load = True
            self.driver.refresh()
            return self.cookies_load

        except Exception:
            print("Cookies have already been loaded")

    def extract_zip(self,zip_file, extract_to):

        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"Arquivo ZIP não encontrado: {zip_file}")

        os.makedirs(extract_to, exist_ok=True)

        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        for file_name in os.listdir(extract_to):
            old_path = os.path.join(extract_to, file_name)

            if os.path.isfile(old_path):
                file_base, file_ext = os.path.splitext(file_name)
                new_name = file_base.upper() + file_ext
                new_path = os.path.join(extract_to, new_name)

                os.rename(old_path, new_path)

if __name__ == "__main__":
    web_scraper = WebScraper()
