import requests
import re
import os
from bs4 import BeautifulSoup

# Function to download a file from a URL
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)

# Function to extract all files and hyperlinks from a website
def extract_files_and_links(url):
    # Make a request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the links and images on the page
    links = soup.find_all("a")
    images = soup.find_all("img")

    # Filter the links to only include those that end with a specific file extension
    file_extensions = [".pdf", ".xls", ".xlsx", ".mp3", ".mp4", ".avi", ".jpg", ".jpeg", ".png"]
    file_links = [link.get("href") for link in links if any(link.get("href").endswith(ext) for ext in file_extensions)]
    file_links += [img.get("src") for img in images if any(img.get("src").endswith(ext) for ext in file_extensions)]

    # Create a folder to store the files
    folder_name = "website_files"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Download each file and save it in the folder
    for file_link in file_links:
        filename = re.search(r"[^/]+$", file_link).group()
        file_path = os.path.join(folder_name, filename)
        download_file(file_link, file_path)

    # Extract all the hyperlinks on the page
    hyperlinks = [link.get("href") for link in links if link.get("href").startswith("http")]

    # Write the hyperlinks to a text file
    with open(os.path.join(folder_name, "hyperlinks.txt"), "w") as file:
        file.write("\n".join(hyperlinks))

# Get the URL from the user
url = input("Enter a URL: ")

# Extract files and hyperlinks from the website
extract_files_and_links(url)
