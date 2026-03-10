from bs4 import BeautifulSoup
import requests
url = "https://pfaf.org/user/Plant.aspx?LatinName=Matricaria+chamomilla"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# Example: Find medicinal section (adjust selector based on page structure)
medicinal = soup.find("h2", text="Medicinal Uses").find_next("p").text
print(medicinal)