
from selenium.webdriver.common.by import *

cokkies_button_e = (By.CSS_SELECTOR, "body > div.dsgov > div > div > div > div > " "div.br-modal-footer.actions > button.br-button"".secondary.small.btn-accept")
download_annex_1 = (By.CSS_SELECTOR, "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(1) > a:nth-child(1)")
download_annex_2 = (By.CSS_SELECTOR, "#cfec435d-6921-461f-b85a-b425bc3cb4a5 > div > ol > li:nth-child(2) > a")

accounting_files_e = (By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(20) > td:nth-child(2) > a")
accounting_files_2_e = (By.CSS_SELECTOR,"body > table > tbody > tr:nth-child(21) > td:nth-child(2) > a")
table_href_e = (By.CSS_SELECTOR, "body > table")
links_e = (By.TAG_NAME, "a")