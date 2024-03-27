from __future__ import annotations

from typing import Generator
from urllib.parse import urljoin

from scrapy import Request, Spider
from scrapy.responsetypes import Response

from ..items import TitleItem


class TitleSpider(Spider):
    """
    Scrapes title pages and enqueues all links found on the page.
    """

    name = 'indeed'

    # The `start_urls` specified in this class will be merged with the `start_urls` value from your Actor input
    # when the project is executed using Apify.
    start_urls = ['https://www.indeed.com/jobs?q=Java&sc=0kf%3Ajt%28contract%29%3B&vjk=1b93328edf307cda']

    def parse(self, response: Response):
       
       job_urls = response.xpath('//*[contains(@class,"resultContent")]')

       for job_url in job_urls:
           
           product_url = urljoin(response.url, job_url)
           yield Request(product_url, callback=self.parse_product)

    def parse_product(self, response: Response):

        job_title = response.xpath('//*[contains(@class,"jobsearch-JobInfoHeader-title")]//span/text()').get()
        company_name = response.xpath('//*[contains(@data-testid,"inlineHeader-companyName")]//a/text()').get()
        address = response.xpath('//*[contains(@data-testid,"companyLocation")]//text()').get()

        job_type_lst =response.xpath('//h3[contains(text(),"Job type")]/following-sibling::ul//div/text()').extract()

        job_type = ''.join([i for i in job_type_lst if i.strip()])

        description = response.xpath('//*[@id="jobDescriptionText"]//text()').extract()

        yield TitleItem(
            url=response.url,
            job_title=job_title,
            company_name=company_name,
            address=address,
            job_type=job_type,
            description=description
        )
        
           
           
           

