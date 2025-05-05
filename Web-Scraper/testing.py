import scrapy # type: ignore
import time

#rohkem_tooteid = True

class BrickSetSpider(scrapy.Spider):
    name = "poe_spider"
    # a list of URLs that you start to crawl from. We'll start with one URL.
    #url = "https://finetrek.ee/et/products-page?groupID=11&records=24&skip=0"
    url = "https://finetrek.ee/et/products-page?groupID=70&records=24&skip=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }

    def start_requests(self):
        # Set the headers here.
        yield scrapy.http.Request(self.url, headers=self.headers)

    def parse(self, response):
        # Lae kõik tooted
        #tooted = response.css("ul.products li")
        #if not tooted:
        #    global rohkem_tooteid
        #    rohkem_tooteid = False
        #    return
        
        for riistad in response.css("ul.products li"):
            """The brickset object we’re looping over has its own css method, 
            so we can pass in a selector to locate child elements
            """
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            #yield {
            #    'name': brickset.css(div.product__name.fw-500::text).extract_first(),
            #    'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            #    'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            #    'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            #}
            yield {
                'name': riistad.css("div.product__name.fw-500::text").extract_first(),
                'price': riistad.css("div.js__product__price::text").extract_first().strip(),
                'stock': riistad.css("dd.in-stock::text").extract_first(),
                'image': riistad.css("img.product__image::attr(src)").extract_first(),
            }

        #if rohkem_tooteid:
        #    time.sleep(5)
        #    yield scrapy.FormRequest(
        #        url=response.url,
        #        method="GET",
        #        callback=self.parse,
        #        dont_filter=True
        #    )

        # define a selector for the "next page" link
        #NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        # extract the first match, and check if it exists
        #next_page = response.css("button.js__products__paginate::attr(style)").extract_first()

        #if next_page:
        #    time.sleep(5)  # to avoid http response 429
        #    url = response.urljoin(next_page)
        #    yield scrapy.Request(url, self.parse, headers=self.headers)

