import requests
from bs4 import BeautifulSoup
import csv
cookie = input('Enter Cookie:')
url = input('Enter URL: ')

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'elogbook.cpsp.edu.pk',
    'Referer': 'https://elogbook.cpsp.edu.pk/eportal/eportal/index.php?app=elogbook',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}
request = requests.get(url=url, verify=False, headers=headers)

soup = BeautifulSoup(request.content, 'html.parser')
table = soup.find('table', {'id': 'dat-tables'})

# Initialize an empty list to store the data
data_list = []

# Find all rows in the table
rows = table.find_all('tr')

# Loop through the rows and extract data
for row in rows:
    columns = row.find_all('td')
    if len(columns) > 1:  # Ensure it's a valid data row
        data = {
            'Number': columns[0].get_text(),
            'Admit Date / Hpt. Reg No': columns[1].get_text(),
            'Diagnosis': columns[2].get_text(),
            'Brief Description': columns[3].find('textarea').get_text(),
            'Competency Group/Details': columns[4].find('table').get_text(),
        }
        data_list.append(data)

# Specify the CSV file name
csv_filename = 'table_data.csv'

# Write the data to a CSV file
with open(csv_filename, 'rw') as csv_file:
    fieldnames = data_list[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    for row in data_list:
        writer.writerow(row)

print(f'Data has been successfully saved to {csv_filename}')
