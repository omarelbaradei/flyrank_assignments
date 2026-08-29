import os
import sys
import requests
cache_dir="cache"

cache_file= os.path.join("cache_dir","catalogue-page-1.html")

url="https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

user_agent= "FlyRankInternship A9/1.0 (+https://github.com/omarelbaradei/web_scraper)"

os.makedirs(cache_dir,exist_ok=True)

if os.path.exists(cache_file):

    with open(cache_file,"r",encoding="utf-8") as file:

        file_content=file.read()

    print("CACHE HIT")

else:

    headers={"user_agent":user_agent}

    try:
        response=requests.get(url,headers=headers,timeout=5)

        if response.status_code!=200:

            print(f"Fetch failed with status code : {response.status_code}")

            sys.exit(0)

        with open(cache_file,"w",encoding="utf-8") as file:

            file.write(response.text)

            print("FETCH")

    except requests.RequestException as e:

        print(f"request failed {e}")

