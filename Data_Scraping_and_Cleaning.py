
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


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
    
    # Collection all recommendation
    for item in soup.find_all("td", {"class": "review-value rating-yes"}):
        recommend.append(item.get_text())    
    for item in soup.find_all("td", {"class": "review-value rating-no"}):
        recommend.append(item.get_text())

# DATA CLEANING :
#----------------------------------------------------------

def clean_reviewtext(text):
    cleaned_text = re.sub(r'✅ Trip Verified |  +|Not Verified +| +|^\s+|\s+$',' ', text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

#----------------------------------------------------------

# Creating a Dataframe for storing the collected data
df = pd.DataFrame()

df["review"] = review

df["review_text"] = review_text

df["review_rating"] = review_rating

df["RECOMMENDED"] = recommend

#----------------------------------------------------------

# Convert review_rating to int
df['REVIEW_RATING'] = df['review_rating'].astype(int)

# Apply the cleaning function to the 'review_text' and 'reviews' column
df['review_text'] = df['review_text'].apply(clean_reviewtext)
df['review'] = df['review'].apply(clean_reviewtext)

# joining two review column to a single column
df['REVIEW_TEXT'] = df['review'] + ' ' + df['review_text']

# Droping the columns
df = df.drop(columns=['review','review_text','review_rating'])

# saving the Scrapped data
df.to_csv("BA_reviews.csv")