import scrapy
from scrapy.http import HtmlResponse


class BillionairesSpider(scrapy.Spider):
    name = "billionaires"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/The_World%27s_Billionaires"]

    def parse(self, response:HtmlResponse):
        years = sorted(set(response.css('span.mw-headline').re(r'\d+')))[::-1]
        tables = response.css("table.wikitable")
        
        for table in tables:
            table_headers = table.css("tr")[0].css("th::text").getall()
            header_rows = {item: item.replace("\n", "") for item in table_headers}
            if len(header_rows) <= 4: continue

            table_body_rows = response.css("table.wikitable").css("tbody").css("tr")
            for table_body_row in table_body_rows: pass

