# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class SoftwareJobsSpider(scrapy.Spider):
    name = 'software_jobs'
    allowed_domains = ["craigslist.org"]
    start_urls = ['https://portland.craigslist.org/search/jjj?query=software/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
        
            yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Address':address})

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
    
        compensation = response.xpath('//p[@class="attrgroup"]/span/b/text()')[0].extract()
        employment_type = response.xpath('//p[@class="attrgroup"]/span/b/text()')[1].extract()
        
        yield{'URL': url, 'Title': title, 'Address':address, 'Compensation':compensation, 'Employment Type':employment_type}
    
