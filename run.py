# Run first.
# usage is
# > python3 run.py

from xml.etree import ElementTree as ET
import requests
import json
import csv
import time

def get_all_IDs():
    '''
    Replace the block below with what you are searching for
    term is how it would look on PubMED
    db is the database
    rt is the format the search will be returned in
    retmax is how many searches to return. I knew ahead of time how many I was looking for
    '''
    # *******************************************
    term = "Wellenius[Author-Last]+G[Author-First]"
    db = 'pubmed'
    rt = "json"
    retmax = 300
    # *******************************************

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db="+ db + \
        "&term=" + term + "&retmode=" + rt + "&bdata=<citations>&retmax=" + str(retmax)

    # Make the GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the XML content
        json_data = json.loads(response.text)
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        json_data = ""

    ID_list = json_data.get("esearchresult").get("idlist")

    return(ID_list)

def get_author_info(ID):

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + str(ID) + \
    "&rettype=xml"

    # Make the GET request to the API
    response = requests.get(url)

    print(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the XML content
        xml_data = response.text
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        xml_data = ""
        return 

    # Corrected XML data (removed leading spaces and lines)
    # xml_data_corrected = xml_data.strip()

    # Parse XML again
    root = ET.fromstring(xml_data)

    # Reset data_rows for the corrected attempt
    data_rows = []

    # Extract year
    year = root.find(".//DateCompleted/Year").text if root.find(".//DateCompleted/Year") is not None else None
    if year == None:
        year = root.find(".//PubDate/Year").text if root.find(".//PubDate/Year") is not None else None

    # Extract all affiliations (assuming only one or unique affiliations per article)
    affiliations = root.findall(".//Affiliation")
    unique_affiliations = list(set(aff.text for aff in affiliations)) if affiliations else ["Unknown"]

    # Process each author
    for author in root.findall(".//Author"):
        last_name = author.find("LastName").text if author.find("LastName") is not None else "Unknown"
        first_name = author.find("ForeName").text if author.find("ForeName") is not None else "Unknown"
        # Assign the first (or only) affiliation to authors without a specific affiliation
        affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else unique_affiliations[0]
        data_rows.append([year, last_name, first_name, affiliation])

    # Prepare the table header
    article_data = [
        {   
            "PMID": ID,
            "DateCompletedYear": row[0],
            "Author Last": row[1],
            "Author First name": row[2],
            "Affiliation": row[3]
        } for row in data_rows
    ]

    return(article_data)


if __name__ == "__main__":
    IDs = get_all_IDs()
    author_data = []
    for ID in IDs:
        author_data.append(get_author_info(ID))
        time.sleep(1)
        
    ## then concatenate into a table
    author_data_flat = [item for row in author_data for item in row]

    # Specify the CSV file name
    csv_file_name = 'articles_authors.csv'

    # Open the file in write mode
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object with "|" as the delimiter
        csv_writer = csv.writer(file, delimiter='|')
        
        # Write the header
        csv_writer.writerow(['PMID', 'DateCompletedYear', 'Author Last', 
                             'Author First name', 'Affiliation'])
        
        # Iterate over each article in the dictionary
        for item in author_data_flat:
            csv_writer.writerow([item['PMID'], 
                                    item['DateCompletedYear'], 
                                    item['Author Last'], 
                                    item['Author First name'], 
                                    item['Affiliation']])
