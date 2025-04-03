import configparser
import time
import zipfile
import os
import pdfplumber
import pandas as pd


class PdfToCSV:

    def __init__(self):

        try:

            self.config = self.load_config()

            self.zip_path = self.config["CSV"]["zip_path"]
            self.out_csv = self.config["CSV"]["out_csv"]
            self.csv_name = self.config["CSV"]["csv_name"]
            self.extension_csv = self.config["EXTENSION"]["csv"]
            self.extension_zip = self.config["EXTENSION"]["zip"]

            self.find_file()
            self.export_csv(self.pdf_path, self.out_csv)
            self.compress_file()

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def load_config():

        config = configparser.ConfigParser()
        config.read("C:\\repo\\intuitive_care\\.config")
        return config

    def find_file(self):

        try:

            for file in os.listdir(self.zip_path):
               if "Anexo_I_" in file:
                    pdf_file = file
                    break

            self.pdf_path = self.zip_path + '\\' + pdf_file
            return self.pdf_path

        except Exception as e:
            print(f"An error occurred: {e}")

    def export_csv(self, pdf_path, csv_path):

        try:

            tables = []

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_table()

                    if page_tables:
                        for table in page_tables:
                            if len(table) > 1:
                                tables.append(table)

            if tables:
                headers = tables[0]
                data = tables[1:]

                df = pd.DataFrame(data, columns=headers)
                df = df.rename(columns={"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"})

                csv_file_path = csv_path + "\\" + self.csv_name +  self.extension_csv
                time.sleep(10)
                df.to_csv(csv_file_path, index=False, encoding='utf-8', sep=';')

        except Exception as e:
            print(f"An error occurred: {e}")

    def compress_file(self):
        try:
            # Caminho do arquivo ZIP final dentro da pasta `out_csv`
            zip_file = os.path.join(self.out_csv, self.csv_name + self.extension_zip)

            with zipfile.ZipFile(zip_file, "w") as zipf:
                for file_name in os.listdir(self.out_csv):
                    file_path = os.path.join(self.out_csv, file_name)

                    if os.path.isfile(file_path) and file_name.endswith(".csv"):
                        zipf.write(file_path, os.path.basename(file_path))

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    pdf_to_csv = PdfToCSV()

