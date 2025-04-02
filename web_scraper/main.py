import time
import os
import requests
import zipfile
import configparser
import re
import json

from  web_scraper.utils.selenium_elements import *
from web_scraper.utils.driver_options import options as chrome_options
from selenium import webdriver

#TODO Melhor os loggins

class Crawler:
    def __init__(self):

        self.config = self.load_config()
        self.url = self.config["SELENIUM"]["url"]
        self.download_dir = self.config["SELENIUM"]["download_dir"]
        self.accounting_folder = self.config["SELENIUM"]["accounting_folder"]
        self.accounting_url = self.config["SELENIUM"]["accounting_url"]
        self.cookies_folder = self.config["SELENIUM"]["cookies_folder"]
        self.extension_zip = self.config["EXTENSION"]["zip"]

        try:

            self.open_driver()
            self.accessing_url()
            self.start_download_annex_1()
            # self.start_download_annex_2()
            # self.accounting_year_1()
            # self.accounting_year_2()
            print("Finalizando")

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

        finally:

            print("Fechando tudo")
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
            time.sleep(3)

            if self.cookies_load is False:
                self.save_cookies()

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def start_download_annex_1(self,):

        try:

            time.sleep(5)
            download_annex = self.driver.find_element(*download_annex_1)
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

            time.sleep(5)
            download_annex = self.driver.find_element(*download_annex_2)
            download_annex.click()

            time.sleep(5)

            self.switch_window()
            self.request_pdf()
            self.close_window()

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

        except Exception as e:

            print(f"An error occurred: {e}")
            self.driver.quit()

    def accounting_year_2(self):

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

    def switch_window(self):

        try:

            attachment = "Anexo"
            handles = self.driver.window_handles

            for handle in handles:

                self.driver.switch_to.window(handle)

                url = self.driver.current_url

                if attachment in url:

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

            download_dir = self.download_dir
            extension_zip = self.extension_zip
            self.create_folder_dir(download_dir)

            url = self.driver.current_url
            response = requests.get(url)

            file_downloaded = os.path.join(download_dir, self.pdf_title)

            if response.status_code == 200:
                with open(file_downloaded, "wb") as file:
                    file.write(response.content)

                match = re.match(r"([A-Za-z]+_[A-Za-z]+)", self.pdf_title)
                file_name = match.group(0)
                file_name = file_name[0].lower() + file_name[1:]

                zip_file = os.path.join(download_dir, file_name + extension_zip)

                with zipfile.ZipFile(zip_file, "w") as zipf:
                    for file_name in os.listdir(download_dir):
                        file_path = os.path.join(download_dir, file_name)
                        if os.path.isfile(file_path) and not file_name.endswith(extension_zip):
                            zipf.write(file_path, os.path.basename(file_path))

                if os.path.exists(file_downloaded):
                    os.remove(file_downloaded)

                print("Download and compression completed successfully!")

            else:

                print(f"Error downloading: {response.status_code}")

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

if __name__ == "__main__":
    crawler = Crawler()
