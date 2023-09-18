
import requests
from bs4 import BeautifulSoup


base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
pages = 30
page_size = 100

review = []
review_text = []
review_rating = []
recommend = []

for i in range(1, pages + 1):

    print(f"Scraping page {i}")

    # Create URL to collect links from paginated data
    url = f"{base_url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

    # Collect HTML data from this page
    response = requests.get(url)

    # Parse content
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')


# DATA COLLECTION :
#----------------------------------------------------------

    # Collecting all main Review
    for item in soup.find_all("h2", {"class": "text_header"}):
        review.append(item.get_text())

    # Collecting all review text
    for item in soup.find_all("div", {"class": "text_content"}):
        review_text.append(item.get_text())

    # Collecting all review rating
    for item in soup.find_all("span", {"itemprop":"ratingValue"}):
        review_rating.append(item.get_text().strip())
        if len(review_rating) == 3000:
            break