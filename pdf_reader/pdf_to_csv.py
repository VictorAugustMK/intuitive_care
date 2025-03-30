import configparser
import zipfile
import os
import pdfplumber
import pandas as pd


class PdfToCSV:

    def __init__(self):

        try:

            self.config = self.load_config()
            self.zip_path = self.config["CSV"]["zip_path"]
            self.extract_folder = self.config["CSV"]["extract_folder"]
            self.out_csv = self.config["CSV"]["out_csv"]
            self.csv_name = self.config["CSV"]["csv_name"]

            self.find_file()
            self.unzip_file(self.pdf_path)
            self.export_csv(self.pdf_path, self.csv_path)
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
                if "anexo_I.zip" in file:
                    file_to_unzip = file
                    break
                else:
                    print("file not found")

            file_path = self.zip_path + '\\' + file_to_unzip

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_folder)

            pdf_files = [f for f in os.listdir(self.extract_folder) if f.endswith(".pdf")]

            if not pdf_files:
                print("not found pdf in zip")
            else:
                pdf_path = os.path.join(self.extract_folder, pdf_files[0])

            self.pdf_path = pdf_path
            return self.pdf_path

        except Exception as e:
            print(f"An error occurred: {e}")

    def unzip_file(self, pdf_path):

        try:

            for file in os.listdir(self.zip_path):
                if "anexo_I.zip" in file:
                    file_to_unzip = file
                    break
                else:
                    print("file not found")

            file_path = self.zip_path + '\\' + file_to_unzip

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_folder)

            pdf_files = [f for f in os.listdir(self.extract_folder) if f.endswith(".pdf")]

            if not pdf_files:
                print("not found pdf in zip")
            else:
                pdf_path = os.path.join(self.extract_folder, pdf_files[0])

            if os.path.isdir(self.out_csv):
                csv_path = os.path.join(self.out_csv, self.csv_name)

            self.pdf_path = pdf_path
            self.csv_path = csv_path

            return self, self.csv_path

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
                df.to_csv(csv_path + ".csv", index=False, encoding='utf-8', sep=';')

        except Exception as e:
            print(f"An error occurred: {e}")

    def compress_file(self):
        try:
            zip_file = os.path.join(self.out_csv, self.csv_name + ".zip")
            with zipfile.ZipFile(zip_file, "w") as zipf:
                for file_name in os.listdir(self.out_csv):
                    file_path = os.path.join(self.out_csv, file_name)
                    if os.path.isfile(file_path) and not file_name.endswith(".zip"):
                        zipf.write(file_path, os.path.basename(file_path))
        except Exception as e:
            print(f"An error occurred: {e}")

pdf_to_csv = PdfToCSV()

