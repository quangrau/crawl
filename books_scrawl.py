import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksScrawlSpider(CrawlSpider):
    name = 'books_scrawl'
    allowed_domains = ['storiestogrowby.org']
    start_urls = ['https://storiestogrowby.org/bedtime-stories-kids-free/']

    rules = (
        # Book Details
        Rule(LinkExtractor(restrict_css='article a.grid-thumbnail'),
             callback='parse_item', follow=False),

        # Next Page
        Rule(LinkExtractor(restrict_css='.pagination .next.page-numbers'), follow=True),
    )

    def parse_item(self, response):
        content = response.css('.so-widget-sow-editor')

        yield {
            "url": response.url,
            "title": response.css('#story-title::text').get(),
            "thumbnail_url": content.css('img::attr(src)').get(),
            "audio_url": content.css('audio > source::attr(src)').get(),
            "images": content.css('img::attr(src)').getall(),
            "raw_content": response.css('.so-widget-sow-editor ::text').getall(),
        }
