# starts crawler with the passed spider. Use below command to run script
# make spider=spider_name scrape 
crawl:
	poetry run scrapy crawl ${spider} -o ./output/${spider}.json

billions:
	$(MAKE) crawl spider=billionaires

nairarate:
	poetry run scrapy crawl nairarate -a start_year=${start_year} -a end_year=${end_year} -o ./output/nairarate.json