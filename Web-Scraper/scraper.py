import scrapy # type: ignore
import sqlite3
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

# Andmebaasi pärimine
def query_db():#query, args=()):#, one=False):
    conn = sqlite3.connect("amblik.db")
    conn.row_factory = sqlite3.Row
    return conn

class RiistaSpider(scrapy.Spider):
    name = "poe_spider"

    start_urls = [
        "https://finetrek.ee/et/products-page?groupID=11&records=24&skip=0",
        "https://finetrek.ee/et/products-page?groupID=70&records=24&skip=0",
        "https://finetrek.ee/et/products-page?groupID=68&records=24&skip=0",
        "https://finetrek.ee/et/products-page?groupID=75&records=24&skip=0",
        "https://finetrek.ee/et/products-page?groupID=90&records=24&skip=0"
        ]

    start_url = [
        "https://finetrek.ee/et/products-page?groupID=11&records=24&skip=0"
        ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }

    def start_requests(self):
        # Set the headers here.
        for url in self.start_urls:
            yield scrapy.http.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        conn = query_db()
        cur = conn.cursor()

        # Extract groupID from query parameters
        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)
        groupID = query_params.get('groupID', [None])[0]  # Get the first groupID value

        for riistad in response.css("ul.products li"):
            name = riistad.css("div.product__name.fw-500::text").extract_first()
            if not name:
                continue

            price = riistad.css("div.js__product__price::text").extract_first()
            if price == None:
                price = 999999999
            else:
                price = price.strip()
            
            stock = riistad.css("dd.in-stock::text").extract_first()
            if not stock:
                stock = "Tellitav"
            
            image = riistad.css("img.product__image::attr(src)").extract_first()
            if not image:
                continue

            cur.execute(
                "INSERT INTO andmed (Name, Price, Stock, image_href, groupID) VALUES (?, ?, ?, ?, ?)", 
                (name, price, stock, image, groupID)
            )
            conn.commit()
        conn.close()

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",  # Suppress Scrapy logs
    })
    process.crawl(RiistaSpider)
    process.start()