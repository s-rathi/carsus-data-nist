import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

# Download data
WEIGHTSCOMP_URL = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

def download_weightscomp(ascii='ascii2', isotype='some'):
    """
    Downloader function for the NIST Atomic Weights and Isotopic Compositions database

    Makes a GET request to download data; then extracts preformatted text

    Parameters
    ----------
    ascii: str
        GET request parameter, refer to the NIST docs
        (default: 'ascii')
    isotype: str
        GET request parameter, refer to the NIST docs
        (default: 'some')

    Returns
    -------
    str
        Preformatted text data

    """
    r = requests.get(url=WEIGHTSCOMP_URL, params={'ascii': ascii, 'isotype': isotype})
    soup = BeautifulSoup(r.text, 'html5lib')
    pre_text_data = soup.pre.get_text()
    pre_text_data = pre_text_data.replace(u'\xa0', u' ')  # replace non-breaking spaces with spaces
    return pre_text_data

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
