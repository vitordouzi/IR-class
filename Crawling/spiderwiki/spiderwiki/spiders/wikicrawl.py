# -*- coding: utf-8 -*-
import scrapy


class WikicrawlSpider(scrapy.Spider):
    name = 'wikicrawl'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/Special:Random/']

    def parse(self, response):
    	yield {
                'title': response.css('title::text').extract_first(),
                'content': ' '.join(response.css('#bodyContent').css('::text').extract()),
            }
    	for new_url in response.css('#bodyContent a[title]::attr(href)').extract():
    		if new_url is not None:
    			yield response.follow(new_url, self.parse)

