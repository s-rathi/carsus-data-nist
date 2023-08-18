import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from carsus.io.nist.ionization import download_ionization_energies


def check_folders(folder_name, file_name):
    """
    Checks if the folder exists and creates it if not.
    
    Parameters:
        folder_name (str): Name of the folder to check/create.
        file_name (str): Name of the file to create inside the folder.
        
    Returns:
        str: The path to the file inside the folder.
    """
    if not os.path.exists(folder_name):  # to check if the folder exists, and create it if not
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)
    return file_path
        
def parse_html_content(html_data):
    """
    Parses the HTML content to extract ionization energy data and saves it to a CSV file.
    
    Parameters:
        html_data (str): The HTML data to parse.
    """
    html_file_path = check_folders('html_files', 'ionization_energies.html')
    with open(html_file_path, "w", encoding="utf-8") as file:  # Save the html data to a file
        file.write(html_data)
    
    soup = BeautifulSoup(html_data, 'html5lib')
    pre_element = soup.find('pre')
    pre_text_data = pre_element.get_text()
    
    rows = pre_text_data.strip().split('\n')

    table_data = []
    for row in rows:
        cells = row.split('|')
        cleaned_cells = [cell.strip() for cell in cells]
        table_data.append(cleaned_cells)
    
    table_data = [row for row in table_data if len(row) > 1] # Remove empty rows

    column = ['At. Num', 'Ion Charge', 'Ground Shells', 'Ground Level', 'Ionization Energy (eV)', 'Uncertainty (eV)', 'x']
    df = pd.DataFrame(table_data[2:], columns=column)
    df = df.drop(df.columns[-1], axis=1)

    csv_file_path = check_folders('nist_data', 'ionization_energies.csv')
    df.to_csv(csv_file_path, index=False)
    return

if __name__ == "__main__":
        ionization_energies = parse_html_content(download_ionization_energies())
