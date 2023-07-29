import requests
import pandas as pd
from bs4 import BeautifulSoup

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

# Save the html content
def save_html(html_file_path):
    html_content=download_weightscomp()
    with open(html_file_path, "w", encoding="utf-8") as file:  # Save the html data to a file
        file.write(html_content)
    return file 

html_file_path='weights.html'
weights_html=save_html(html_file_path)

# Format the data
def parse_html_content(html_content):
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
    return data

data = parse_html_content(download_weightscomp())
df = pd.DataFrame(data)
df = df.iloc[2:]

# Save the DataFrame to CSV file
csv_file_path='nist_atomic_weights.csv'
df.to_csv(csv_file_path, index=False)
