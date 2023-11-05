# starts crawler with the passed spider. Use below command to run script
# make spider=spider_name scrape 
crawl:
	poetry run scrapy crawl ${spider} -o ./output/${spider}.jsonl