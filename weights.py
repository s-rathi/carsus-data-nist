import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from carsus.io.nist.weightscomp import download_weightscomp


# Check and create a path to save files
def check_folders(folder_name, file_name):
    if not os.path.exists(folder_name):  # to check if the folder exists, and create it if not
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)
    return file_path
    
# Format the data
def parse_html_content(html_content):
    html_file_path = check_folders('html_files', 'weights.html')
    with open(html_file_path, "w", encoding="utf-8") as file:   # Save the html data to a file
        file.write(html_content)
        
    data = []
    lines = html_content.strip().split('\n')
    entry = {}
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            entry[key.strip()] = value.strip()
        else:
            data.append(entry)
            entry = {}
    
    data.append(entry)  # Append the last entry    
    df = pd.DataFrame(data)
    df = df.iloc[2:]

    csv_file_path = check_folders('nist_data', 'weights.csv')
    df.to_csv(csv_file_path, index=False)
    return
        
atomic_weights = parse_html_content(download_weightscomp())
