import requests
from bs4 import BeautifulSoup
import pandas as pd

IONIZATION_ENERGIES_URL = 'https://physics.nist.gov/cgi-bin/ASD/ie.pl'

def download_ionization_energies(
        spectra='h-uuh',
        e_out=0,
        e_unit=1,
        format_=1,
        at_num_out=True,
        sp_name_out=False,
        ion_charge_out=True,
        el_name_out=True,
        seq_out=False,
        shells_out=True,
        conf_out=False,
        level_out=True,
        ion_conf_out=False,
        unc_out=True,
        biblio=False):
    """
        Downloader function for the Ionization Energies Data from the NIST Atomic Spectra Database
        Parameters
        ----------
        spectra: str
            (default value = 'h-uuh')
        Returns
        -------
        str
            Preformatted text data
        """
    data = {'spectra': spectra, 'units': e_unit,
            'format': format_, 'at_num_out': at_num_out, 'sp_name_out': sp_name_out,
            'ion_charge_out': ion_charge_out, 'el_name_out': el_name_out,
            'seq_out': seq_out, 'shells_out': shells_out, 'conf_out': conf_out,
            'level_out': level_out, 'ion_conf_out': ion_conf_out, 'e_out': e_out,
            'unc_out': unc_out, 'biblio': biblio}

    data = {k: v for k, v in data.items() if v is not False}
    data = {k:"on" if v is True else v for k, v in data.items()}
   
    r = requests.post(url=IONIZATION_ENERGIES_URL, data=data)
    return r.text

def parse_html_content(html_file_path):
    
    html_data=download_ionization_energies()
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

    column=['At. Num', 'Ion Charge', 'El. Name', 'Ground Shells', 'Ground Level', 'Ionization Energy (eV)', 'Uncertainty (eV)','x']
    df = pd.DataFrame(table_data[2:], columns=column)
    df = df.drop(df.columns[-1], axis=1)
    return df

file_path='ionization.html'
csv_file_path='ionization_energies.csv'
ionization_data=parse_html_content(file_path)
ionization_data.to_csv(csv_file_path, index=False) # Save the DataFrame to a CSV file    
