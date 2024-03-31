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
    start_urls = ['https://www.linkedin.com/jobs/search/?currentJobId=3875742938&f_I=14%2C11%2C1%2C148%2C43%2C31%2C4%2C1594%2C15%2C116%2C84&f_JT=F%2CC%2CT&geoId=103644278&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R']

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
        
           
           
           

