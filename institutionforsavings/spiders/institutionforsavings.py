import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from institutionforsavings.items import Article


class institutionforsavingsSpider(scrapy.Spider):
    name = 'institutionforsavings'
    start_urls = ['https://www.institutionforsavings.com/news']

    def parse(self, response):
        articles = response.xpath('//div[@class="card accordion remove-blank"][descendant::a]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            meta = article.xpath('.//div[contains(@data-content-block, "accordionHeader")]//text()').getall()
            meta = [text.strip() for text in meta if text.strip() and '{' not in text]
            title = meta[0]
            date = meta[1]

            content = article.xpath('.//div[@class="card-body content"]//text()').getall()
            content = [text for text in content if text.strip() and '{' not in text]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



