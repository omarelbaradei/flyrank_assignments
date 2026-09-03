import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime, timezone

cache_dir="cache"

def fetch(current_url,page_num,book_num=0):

    if book_num == 0:

        cache_file= os.path.join(cache_dir,f"catalogue-page-{page_num}.html")

    else:
        cache_file=os.path.join(cache_dir,f"book_number_{book_num}_content_of_catalogue-page-{page_num}.html")

    user_agent= "FlyRankInternship A9/1.0 (+https://github.com/omarelbaradei/web_scraper)"

    os.makedirs(cache_dir,exist_ok=True)

    if os.path.exists(cache_file):

        with open(cache_file,"r",encoding="utf-8") as file:

            file_content=file.read()

        print("CACHE HIT")

        return file_content

    else:

        headers={"User-Agent":user_agent}

        try:
            response=requests.get(current_url,headers=headers,timeout=5)

            if response.status_code!=200:

                response.raise_for_status()
                

            with open(cache_file,"w",encoding="utf-8") as file:

                file.write(response.text)

                # print("FETCH")

                return response.text

        except requests.RequestException as e:

            print(f"an error has ocurred :{e}")
    

def parse_file(current_url,page_num):

    cache_file= os.path.join(cache_dir,f"catalogue-page-{page_num}.html")

    if os.path.exists(cache_file):

        with open (cache_file , "r",encoding="utf-8") as file:

            html=file.read()
    else:
        raise FileNotFoundError("not found")

    soup=BeautifulSoup(html,"html.parser")

    absolute_links=[]

    for a_tag in soup.select("h3 a[href]"):

        relative_href= a_tag["href"]

        absolute_href=urljoin(current_url,relative_href)

        absolute_links.append(absolute_href)

    unique_links=set(absolute_links)


    next_button = soup.select_one("li.next a[href]")

    if next_button:
        
        next_relative_url = next_button["href"]
      
        current_url = urljoin(current_url, next_relative_url)

        time.sleep(1)

    else:

        current_url=None

    
    return {"catalogue_pages" :page_num , "discovered" : len(absolute_links) , "unique_urls" : len(unique_links), "current_url" : current_url}


def parse_book(current_url,source_page,page_num,book_num,fetched_at_iso):

    cache_file=os.path.join(cache_dir,f"book_number_{book_num}_content_of_catalogue-page-{page_num}.html")

    if os.path.exists(cache_file):

        with open(cache_file,"r",encoding="utf-8") as book:

            book_content=book.read()

    else:

        raise FileNotFoundError("not found")

    soup=BeautifulSoup(book_content,"html.parser")

    product_main=soup.select_one("div.product_main")

    if not product_main:

        print("product area not found in this page")

        return None

    title_tag=product_main.select_one("h1")

    title=None

    if title_tag:

        title=title_tag.get_text(strip=True)

    price_tag=product_main.select_one("p.price_color")

    price=None

    if price_tag:

        price = price_tag.get_text(strip=True)


    availability_tag=product_main.select_one("p.instock")

    availability=None

    if availability_tag:

        availability=availability_tag.get_text(strip=True)


    rating_tag = product_main.select_one("p.star-rating")

    rating_text = None

    if rating_tag:

        classes = rating_tag.get("class", [])
    
        rating_classes = [c for c in classes if c != "star-rating"]

        if rating_classes:

            rating_text = rating_classes[0]

    desc_header = soup.select_one("#product_description")

    description = None

    if desc_header:

        desc_p = desc_header.find_next_sibling("p")

        if desc_p:

            description = desc_p.get_text(strip=True)

    return {
        "title": title,
        "product_url": current_url,
        "price_text": price,
        "availability_text": availability,
        "rating_text": rating_text,
        "description": description,  
        "source_page": source_page,
        "fetched_at": fetched_at_iso,
    }    

    


    

    
        





def scrape(current_url:str,pages_num:list):

        parsed_links_in_all_pages=[]

        for page_num in pages_num:

            fetched_page=fetch(current_url,page_num)

            parsed_links=parse_file(current_url,page_num)

            parsed_links_in_all_pages.append(parsed_links)

            current_url=parsed_links["current_url"]

            if current_url is None:

                return  parsed_links_in_all_pages,"no more pages to parse 🔚🤷🏼"

        return parsed_links_in_all_pages
            

         
#print(scrape("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",list(range(1,5))))
fetch("https://books.toscrape.com/catalogue/sharp-objects_997/index.html",1,1)
current_time=datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
print(parse_book("" \
"https://books.toscrape.com/catalogue/sharp-objects_997/index.html","https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
1,1,current_time))   



