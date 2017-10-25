import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spiderwiki.items import SpiderwikiItem

class WikiCrawler(CrawlSpider):
	name = 'wikicrawler'
	allowed_domains = ['en.wikipedia.org']
	start_urls = ['http://en.wikipedia.org/wiki/Web_crawler']
	#start_urls = ['http://en.wikipedia.org/wiki/Special:Random/']
	linkextractor = LinkExtractor(allow=('wiki/', ), restrict_css=('#bodyContent', ), deny=('wiki/Category:', 'Special:', '#', ) )

	rules = ( Rule(linkextractor, callback='parse_item', follow=True), )

	def parse_item(self, response):
		item = SpiderwikiItem()
		item['url'] = response.url
		item['title'] = response.css('title::text').extract_first()
		item['content'] = ' '.join(response.css('#bodyContent').css('::text').extract())
		item['urls'] = set()
		for link in self.linkextractor.extract_links(response):
			item['urls'].add(link.url)
		yield item
