import scrapy
from ..items import WorldRichestItem
from scrapy.http import HtmlResponse
from scrapy.utils.log import logger


class BillionairesSpider(scrapy.Spider):
    name = "billionaires"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/The_World%27s_Billionaires"]

    def parse(self, response: HtmlResponse):
        years = sorted(set(response.css("span.mw-headline").re(r"\d+")))[::-1]
        tables = response.css("table.wikitable")
        counter = 0
        for table in tables:
            table_headers = table.css("tr")[0].css("th::text").getall()
            header_rows = {item: item.replace("\n", "") for item in table_headers}

            # any table header whose header row is not greater than 4 columns
            # is not the kind of table targetted, we immeidately proceed to
            # the next table
            if len(header_rows) < 4:
                continue

            year = years[counter]
            counter += 1
            table_body_rows = table.css("tbody").css("tr")
            for table_body_row in table_body_rows:
                row_data = table_body_row.css("td")
                items = []
                for col in row_data:
                    col_inner_text = col.css("::text").get()
                    items.append(col_inner_text)

                if len(items) != 4:
                    continue

                position = items[0]
                name = items[1]
                networth = items[2]
                age = items[3] if len(items) > 4 else "N/A"
                company = items[5] if len(items) > 4 else "N/A"

                yield WorldRichestItem(
                    year=year,
                    position=position,
                    name=name,
                    networth=networth,
                    age=age,
                    company=company,
                )
