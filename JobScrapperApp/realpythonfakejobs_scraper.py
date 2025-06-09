import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Get url from fake python jobs site
url = 'https://realpython.github.io/fake-jobs/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

job_elements = soup.find_all("div", class_="card-content")

# Prepare list to store jobs
job_data = []

for job_elem in job_elements:
    title_elem = job_elem.find("h2", class_="title")
    company_elem = job_elem.find("h3", class_="company")
    location_elem = job_elem.find("p", class_="location")
    link_elem = job_elem.find_all("a")[1] # Need to get 2nd <a>

    if None in (title_elem, company_elem, location_elem, link_elem):
        continue

    # Filter for python jobs
    if 'python' in title_elem.text.lower():
        job_data.append({
            'Title': title_elem.text.strip(),
        'Company': company_elem.text.strip(),
        'Location': location_elem.text.strip(),
        'URL': link_elem['href']
       })

# Save to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'fake_python_jobs_{timestamp}.csv'

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Company', 'Location', 'URL'])
    writer.writeheader()
    for job in job_data:
        writer.writerow(job)
for job in job_data[:3]:
    print(f"{job.get('company')} – {job.get('Title')}: {job.get('URL')}")

print(f"\nSaved {len(job_data)} Python jobs to {filename}")
