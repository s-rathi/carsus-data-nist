import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from common_utils import check_folders
from carsus.io.nist.weightscomp import download_weightscomp


# Format the data
def parse_weights_html_content(html_content):
    """
    Parses the HTML content and saves the data as CSV.
    Parameters
    ----------
    html_content : str
        The preformatted HTML content.
    Returns
    -------
    None
    """
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

if __name__ == "__main__":
    atomic_weights = parse_weights_html_content(download_weightscomp())
