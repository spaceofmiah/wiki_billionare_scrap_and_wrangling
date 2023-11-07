import re
import scrapy
import calendar
from arrow import Arrow
from datetime import datetime
from ..items import NairaRateItem
from scrapy.http import HtmlResponse


class NairaRateSpider(scrapy.Spider):
    name = "nairarate"  # naira rates
    allowed_domains = ["www.naijanews.com"]

    def start_requests(self):
        self.routes = self.retrieve_next_route()
        yield scrapy.Request(next(self.routes), self.parse)

    def get_day_suffix(self, day: int) -> str:
        """
        Returns the suffix for a given day.
        """
        if day in [11, 12, 13]:
            return "th"
        else:
            return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def retrieve_next_route(self):
        RESOURCE_START_YEAR = 2022
        # retrieve attributes passed by tags and set default if nothing is gotten
        start_year: str = getattr(self, "start_year", datetime.now().year)
        end_year: str = getattr(self, "end_year", datetime.now().year)

        if not start_year.isdigit() and len(start_year) != 4:
            start_year = RESOURCE_START_YEAR
        else:
            start_year = (
                RESOURCE_START_YEAR if int(start_year) < 2022 else int(start_year)
            )

        now = datetime.now()

        if not end_year.isdigit() and len(end_year) != 4:
            end_year = now.year
        else:
            end_year = (
                datetime.now().year if int(end_year) > now.year else int(end_year)
            )

        # compute date for the passed year
        if start_year == RESOURCE_START_YEAR:
            # resource starts tracking from October 4th
            start_day = 4
            start_month = 10
        else:
            start_day = 1
            start_month = 1

        if end_year == now.year:
            end_month = now.month
            end_day = now.day
        else:
            end_month = 12
            end_day = calendar.monthrange(year=start_year, month=1)[1]

        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)

        # generate dates between the start date and end date
        dates = Arrow.range(frame="days", start=start_date, end=end_date)
        for date in dates:
            numeric_date = date.strftime("%Y/%m/%d")
            full_date = date.strftime(
                f"{date.day}{self.get_day_suffix(date.day)}-%B-%Y"
            ).lower()
            yield f"https://www.naijanews.com/{numeric_date}/black-market-dollar-to-naira-exchange-rate-today-{full_date}/"

    # @classmethod
    # def update_settings(cls, settings):
    #     super().update_settings(settings)
    #     settings.set("DOWNLOAD_DELAY", 2.5, priority="spider")

    def parse(self, response: HtmlResponse):
        # Extraction -- Parse HTML

        # page being extracted has two tables:
        #  - black market buy & sell rate
        #  - cbn buy & sell rate
        # script utilizes the first table which is the black market rate

        table = response.css("table")[0]  # black market table on first index

        # Table has no thead only tbody and the first row in the table body
        # is the header of the table. Hence, we need to skip the first row
        table_body_rows = table.css("tbody").css("tr")[1:]
        data_items = table_body_rows.css("td::text").getall()
        date = re.findall(r"\d+/\d+/\d+", response.url)[0]

        for route in self.routes:
            yield scrapy.Request(route, callback=self.parse)

        yield NairaRateItem(
            date=date,
            buy_rate=data_items[1], 
            sell_rate=data_items[-1],
        )
