import requests
from bs4 import BeautifulSoup  #BeautifulSoup → extract info from HTML
import re
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


url = "https://quotes.toscrape.com/"
response = requests.get(url)

print(response.status_code)   # 200 (success)
# print(response.json())

            #"html.parser" → built-in parser that understands HTML structure.
soup = BeautifulSoup(response.text, "html.parser")  #res.text → gives the raw HTML content as a string.
                                        #soup acts like a tree structure of the webpage.

# Find all quotes
quotes = soup.find_all("span", class_="text")
for q in quotes:
    print(q.text)


raw = "  Price: $1,299.00!!  "
clean = raw.strip()             # remove extra spaces
clean = re.sub(r"[^0-9.]", "", clean)  # keep only numbers
print(float(clean))             # 1299.00

try:
    res = requests.get("https://quotes.toscrape.com/404")
    res.raise_for_status()  # raises exception if status != 200
except requests.exceptions.RequestException as e: # to catch  any request related exceptions
    print("Error:", e)


try:
    session = requests.Session() #session  is to send requests
    retry = Retry( total=3, #total=3 → retry 3 times
                backoff_factor=1, #backoff_factor=1 → wait 1s, 2s, 4s...
                    status_forcelist=[500, 502, 503, 504]) #status_forcelist → retry on server errors
    adapter = HTTPAdapter(max_retries=retry) #adapter creates an HTTP adapter that automatically handles retries
    session.mount("http://", adapter) # syntax--.mount(prefix, adapter)
    session.mount("https://", adapter) #mount() attaches an adapter to a specific URL prefix.
    res = session.get("https://quotes.toscrape.com/500")
    print(res.status_code)
except requests.exceptions.RequestException as e: # to catch  any request related exceptions
    print("Error:", e)
