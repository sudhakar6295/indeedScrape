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
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2, # 2 seconds of delay
        "CONCURRENT_REQUESTS" : 1,
        "ROBOTSTXT_OBEY" : False,
        "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
          }

    name = 'indeed'

    # The `start_urls` specified in this class will be merged with the `start_urls` value from your Actor input
    # when the project is executed using Apify.
    start_urls = ['https://www.linkedin.com/jobs/search/?currentJobId=3875742938&f_I=14%2C11%2C1%2C148%2C43%2C31%2C4%2C1594%2C15%2C116%2C84&f_JT=F%2CC%2CT&geoId=103644278&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R']

    def parse(self, response: Response):
       
       job_urls = response.xpath('//*[@data-tracking-control-name="public_jobs_jserp-result_search-card"]/@href').extract()

       for job_url in job_urls:

           yield Request(job_url, callback=self.parse_product)

    def parse_product(self, response: Response):

        job_title = response.xpath('//*[@data-tracking-control-name="public_jobs_topcard-title"]/h2/text()').get()
        company_name = response.xpath('//*[@data-tracking-control-name="public_jobs_topcard-org-name"]/text()').get()


        yield TitleItem(
            url=response.url,
            job_title=job_title,
            company_name=company_name,

        )
        
           
           
           

